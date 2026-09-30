"""Browser checks. Generate native reference cases ONLY in an isolated CI/container."""

import argparse
import hashlib
import json
from pathlib import Path


def observation_hash(observation):
    fields = [observation[key] for key in ("frames", "state", "level_index", "available_actions", "full_reset")]
    return hashlib.sha256(json.dumps(fields, separators=(",", ":")).encode()).hexdigest()


def write_golden(output):
    # This branch executes native Python. Never run it on a personal host.
    from arc3_synthetic_games.dataset import catalog
    from arc3_synthetic_games.native import NativeGame

    cases = []
    for entry in catalog()["games"]:
        game = NativeGame(entry["id"])
        events = []
        for level in range(7):
            observation = game.select_level(level)
            events.append({"operation": "level", "body": {"level": level}, "sha256": observation_hash(observation)})
            for action in entry["controls"]:
                if observation["state"] in ("WIN", "GAME_OVER"):
                    break
                if action not in observation["available_actions"]:
                    continue
                data = {"x": 32, "y": 32} if action == 6 else {}
                observation = game.act(action, data)
                events.append({"operation": "action", "body": {"action_id": action, "data": data},
                               "sha256": observation_hash(observation)})
            for operation in ("reset",):
                observation = getattr(game, operation)()
                events.append({"operation": operation, "body": {}, "sha256": observation_hash(observation)})
        observation = game.restart()
        events.append({"operation": "restart", "body": {}, "sha256": observation_hash(observation)})
        cases.append({"id": entry["id"], "events": events})
    output.write_text(json.dumps(cases), encoding="utf-8")
    print(f"Native reference: {len(cases)} games, {sum(len(c['events']) for c in cases)} observations")


def check(url, golden, screenshot_dir=None, executable=None):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        options = {"headless": True}
        if executable:
            options["executable_path"] = executable
        browser = playwright.chromium.launch(**options)
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        page.set_default_timeout(180000)
        errors, requests = [], []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: requests.append((request.url, request.method)))
        page.goto(url)
        page.locator(".game-card").last.wait_for()
        assert page.locator(".game-card").count() == 30
        # Lazy-loaded gallery images need to enter the viewport.
        for image in page.locator(".preview img").all():
            image.scroll_into_view_if_needed()
            image.evaluate("img => img.decode()")
        assert not any(".gif" in address for address, _ in requests)
        assert not any("pyodide" in address for address, _ in requests)
        if screenshot_dir:
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            page.evaluate("window.scrollTo(0, 0)")
            page.screenshot(path=str(screenshot_dir / "browser-gallery.png"))
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.screenshot(path=str(screenshot_dir / "browser-gallery-mobile.png"))
            page.set_viewport_size({"width": 1440, "height": 1000})
        page.route("**/browser/arcengine-*.whl", lambda route: route.fulfill(body=b"corrupt"))
        page.locator("button[aria-label^='Play']").first.click()
        page.wait_for_function("document.querySelector('#notice').textContent.includes('checksum mismatch')")
        assert page.locator("#library").is_visible()
        page.unroute("**/browser/arcengine-*.whl")
        page.locator("button[aria-label^='Play']").first.click()
        page.locator("#player").wait_for(state="visible")
        page.wait_for_function("!document.querySelector('#reset').disabled")
        page.locator("#board").focus()
        for key in ("ArrowRight", "Space", "KeyZ"):
            page.keyboard.press(key)
            page.wait_for_function("!document.querySelector('#reset').disabled")
        page.select_option("#level", "6")
        page.wait_for_function("!document.querySelector('#reset').disabled")
        assert page.locator("#level").input_value() == "6"
        page.locator("#reset").click()
        page.wait_for_function("!document.querySelector('#reset').disabled")
        assert page.locator("#level").input_value() == "6"
        page.locator("#restart").click()
        page.wait_for_function("!document.querySelector('#reset').disabled")
        assert page.locator("#level").input_value() == "0"
        page.locator("#mechanics summary").click()
        page.wait_for_function("document.querySelector('#mechanics-text').textContent.length > 0")
        page.locator("#demo summary").click()
        page.wait_for_function("document.querySelector('#demo-image').getAttribute('src')")
        page.locator("#demo-image").evaluate("img => img.decode()")
        if screenshot_dir:
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_dir / "browser-player.png"), full_page=True)
        page.locator("#back").click()
        page.locator("#library").wait_for(state="visible")
        # Compare native state and every pixel after real representative actions.
        count = page.evaluate("""async cases => {
          const api = window.arc3Transport.request;
          let count = 0;
          for (const game of cases) {
            const {session_id} = await api('/api/sessions', 'POST', {game_id: game.id});
            for (const event of game.events) {
              const obs = await api(`/api/sessions/${session_id}/${event.operation}`, 'POST', event.body);
              const value = JSON.stringify([obs.frames, obs.state, obs.level_index, obs.available_actions, obs.full_reset]);
              const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
              const hash = [...new Uint8Array(bytes)].map(v => v.toString(16).padStart(2, '0')).join('');
              if (hash !== event.sha256) throw new Error(`${game.id} ${event.operation}: native/browser mismatch`);
              count++;
            }
            await api(`/api/sessions/${session_id}`, 'DELETE');
          }
          return count;
        }""", json.loads(golden.read_text(encoding="utf-8")))
        # Exercise scaled click input through the actual shared UI.
        page.locator("#search").fill("sg18")
        page.locator(".game-card button").click()
        page.locator("#player").wait_for(state="visible")
        page.wait_for_function("!document.querySelector('#reset').disabled")
        page.evaluate("""() => {
          const original = window.arc3Transport.request;
          window.arc3Transport.request = (...args) => {
            if (args[0].endsWith('/action')) window.lastCheckedAction = args[2];
            return original(...args);
          };
        }""")
        width = page.locator("#board").bounding_box()["width"]
        page.locator("#board").click(position={"x": 180, "y": 180})
        page.wait_for_function("!document.querySelector('#reset').disabled")
        assert page.evaluate("window.lastCheckedAction") == {
            "action_id": 6, "data": {"x": int(180 / width * 64), "y": int(180 / width * 64)}
        }
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        if screenshot_dir:
            page.screenshot(path=str(screenshot_dir / "browser-mobile.png"), full_page=True)
        assert page.evaluate("localStorage.length === 0 && sessionStorage.length === 0")
        assert context.cookies() == []
        assert all(method == "GET" for _, method in requests), "Gameplay should not send HTTP requests"
        assert not errors, errors
        print(f"Browser passed: 30 games, 210 levels, {count} exact native observations, UI and mobile checks")
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-golden", type=Path)
    parser.add_argument("--url", default="http://127.0.0.1:8782/arc3-synthetic-games/")
    parser.add_argument("--golden", type=Path)
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--executable")
    args = parser.parse_args()
    if args.write_golden:
        write_golden(args.write_golden)
    elif args.golden:
        check(args.url, args.golden, args.screenshots, args.executable)
    else:
        parser.error("Choose --golden or --write-golden (isolated native execution only)")
