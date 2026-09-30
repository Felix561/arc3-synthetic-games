"use strict";
const $ = (id) => document.getElementById(id);
const state = {
  games: [],
  game: null,
  session: null,
  csrf: null,
  observation: null,
  busy: false,
  epoch: 0,
};
const colors = [
  "FFFFFF",
  "CCCCCC",
  "999999",
  "666666",
  "333333",
  "000000",
  "E53AA3",
  "FF7BCC",
  "F93C31",
  "1E93FF",
  "88D8F1",
  "FFDC00",
  "FF851B",
  "921231",
  "4FCC30",
  "A356D6",
].map((h) => [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)));
const labels = {
  1: "↑",
  2: "↓",
  3: "←",
  4: "→",
  5: "Space",
  6: "Click",
  7: "Undo · Z",
};
const keys = {
  ArrowUp: 1,
  ArrowDown: 2,
  ArrowLeft: 3,
  ArrowRight: 4,
  Space: 5,
  KeyZ: 7,
};
function node(tag, text, className) {
  const n = document.createElement(tag);
  if (text !== undefined) n.textContent = text;
  if (className) n.className = className;
  return n;
}
function notice(text = "") {
  $("notice").textContent = text;
  $("notice").hidden = !text;
}
async function api(path, method = "GET", body) {
  if (window.arc3Transport)
    return window.arc3Transport.request(path, method, body);
  const options = {
    method,
    credentials: "same-origin",
    cache: "no-store",
    headers: {},
  };
  if (method !== "GET") {
    options.headers = {
      "Content-Type": "application/json",
      "X-CSRF-Token": state.csrf,
    };
    options.body = JSON.stringify(body || {});
  }
  const r = await fetch(path, options);
  let data;
  try {
    data = await r.json();
  } catch {
    throw new Error(
      "The local player did not respond. Check that it is running.",
    );
  }
  if (!r.ok)
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "The request could not be completed.",
    );
  return data;
}
function controlLabel(g) {
  const a = g.controls;
  return [
    a.some((x) => x >= 1 && x <= 4) ? "Arrows" : null,
    a.includes(5) ? "Space" : null,
    a.includes(6) ? "Click" : null,
  ]
    .filter(Boolean)
    .join(" · ");
}
function renderGallery() {
  const query = $("search").value.trim().toLowerCase();
  $("gallery").replaceChildren();
  let count = 0;
  for (const game of state.games) {
    if (!`${game.id} ${game.title}`.toLowerCase().includes(query)) continue;
    count++;
    const card = node("article", undefined, "game-card");
    const imageBox = node("div", undefined, "preview");
    const image = node("img");
    image.src = new URL(game.preview, document.baseURI).href;
    image.alt = `${game.title}, first level`;
    image.width = 256;
    image.height = 256;
    image.loading = "lazy";
    imageBox.append(image);
    const copy = node("div", undefined, "card-copy");
    copy.append(
      node("p", `${game.id.toUpperCase()} / 7 LEVELS`, "card-id"),
      node("h3", game.title),
      node("p", game.teaser, "teaser"),
    );
    const bottom = node("div", undefined, "card-bottom");
    const play = node("button", "Play");
    play.type = "button";
    play.setAttribute("aria-label", `Play ${game.title}`);
    play.addEventListener("click", () => start(game));
    bottom.append(node("span", controlLabel(game), "control-tag"), play);
    copy.append(bottom);
    card.append(imageBox, copy);
    $("gallery").append(card);
  }
  $("no-results").hidden = count !== 0;
}
function syncControls() {
  const terminal =
    state.observation && ["WIN", "GAME_OVER"].includes(state.observation.state);
  const allowed = state.observation?.available_actions || [];
  for (const b of document.querySelectorAll("[data-action]"))
    b.disabled =
      state.busy || terminal || !allowed.includes(Number(b.dataset.action));
  for (const id of ["reset", "restart", "level", "back"])
    $(id).disabled = state.busy;
  $("board").classList.toggle(
    "can-click",
    !state.busy && !terminal && allowed.includes(6),
  );
}
function draw(frame) {
  const ctx = $("board").getContext("2d");
  const data = ctx.createImageData(64, 64);
  for (let y = 0; y < 64; y++)
    for (let x = 0; x < 64; x++) {
      const c = colors[frame[y][x]],
        p = (y * 64 + x) * 4;
      data.data[p] = c[0];
      data.data[p + 1] = c[1];
      data.data[p + 2] = c[2];
      data.data[p + 3] = 255;
    }
  ctx.putImageData(data, 0, 0);
}
async function present(observation, epoch) {
  const frames = observation.frames;
  for (let i = 0; i < frames.length; i++) {
    if (epoch !== state.epoch) return;
    draw(frames[i]);
    if (i < frames.length - 1)
      await new Promise((r) => setTimeout(r, 1000 / state.game.default_fps));
  }
  if (epoch !== state.epoch) return;
  state.observation = observation;
  $("level").value = String(observation.level_index);
  $("game-state").textContent =
    observation.state === "WIN"
      ? "Game complete. Explore another level or restart."
      : observation.state === "GAME_OVER"
        ? "Try this level again with Reset level."
        : `Level ${observation.level_index + 1} of 7 · Experiment with the available actions.`;
}
async function perform(path, body = {}) {
  if (state.busy || !state.session) return;
  state.busy = true;
  syncControls();
  notice();
  const epoch = state.epoch;
  try {
    const observation = await api(
      `/api/sessions/${state.session}/${path}`,
      "POST",
      body,
    );
    await present(observation, epoch);
  } catch (e) {
    notice(e.message);
  } finally {
    if (epoch === state.epoch) {
      state.busy = false;
      syncControls();
      $("board").focus({ preventScroll: true });
    }
  }
}
async function start(game) {
  if (state.busy) return;
  state.busy = true;
  notice();
  const epoch = ++state.epoch;
  try {
    if (state.session) await api(`/api/sessions/${state.session}`, "DELETE");
    state.session = null;
    const result = await api("/api/sessions", "POST", {
      game_id: game.id,
      level: 0,
    });
    state.game = game;
    state.session = result.session_id;
    state.observation = null;
    $("library").hidden = true;
    $("player").hidden = false;
    $("game-id").textContent =
      game.id.toUpperCase() + " / INDEPENDENT SYNTHETIC GAME";
    $("game-title").textContent = game.title;
    $("game-teaser").textContent = game.teaser;
    $("level").replaceChildren(
      ...Array.from({ length: 7 }, (_, i) => {
        const o = node("option", `Level ${i + 1}`);
        o.value = String(i);
        return o;
      }),
    );
    $("actions").replaceChildren();
    for (const action of game.controls) {
      if (action === 6) {
        $("actions").append(node("span", "Click the board", "muted"));
        continue;
      }
      const b = node("button", labels[action], action >= 5 ? "wide" : "");
      b.type = "button";
      b.dataset.action = String(action);
      b.title = `ACTION${action}`;
      b.addEventListener("click", () =>
        perform("action", { action_id: action, data: {} }),
      );
      $("actions").append(b);
    }
    $("mechanics").open = false;
    $("mechanics-text").textContent = "";
    $("demo").open = false;
    $("demo").hidden = !game.demo;
    $("demo-image").removeAttribute("src");
    await present(result.observation, epoch);
    window.scrollTo({ top: 0, behavior: "instant" });
  } catch (e) {
    notice(e.message);
  } finally {
    state.busy = false;
    syncControls();
    if (state.session) $("board").focus({ preventScroll: true });
  }
}
$("back").addEventListener("click", async () => {
  if (state.busy) return;
  state.busy = true;
  syncControls();
  try {
    if (state.session) await api(`/api/sessions/${state.session}`, "DELETE");
  } catch (e) {
    notice(e.message);
  } finally {
    state.epoch++;
    state.session = null;
    state.game = null;
    state.observation = null;
    state.busy = false;
    $("player").hidden = true;
    $("library").hidden = false;
    $("demo-image").removeAttribute("src");
    syncControls();
  }
});
$("level").addEventListener("change", () =>
  perform("level", { level: Number($("level").value) }),
);
$("reset").addEventListener("click", () => perform("reset"));
$("restart").addEventListener("click", () => perform("restart"));
$("search").addEventListener("input", renderGallery);
$("mechanics").addEventListener("toggle", async () => {
  if (!$("mechanics").open || !state.game || $("mechanics-text").textContent)
    return;
  const game = state.game;
  try {
    const result = await api(`/api/games/${game.id}/mechanics`);
    if (state.game === game) $("mechanics-text").textContent = result.text;
  } catch (e) {
    notice(e.message);
  }
});
$("demo").addEventListener("toggle", () => {
  if ($("demo").open && state.game?.demo)
    $("demo-image").src = new URL(state.game.demo, document.baseURI).href;
  else $("demo-image").removeAttribute("src");
});
$("board").addEventListener("click", (e) => {
  if (
    state.busy ||
    !state.session ||
    !state.observation?.available_actions.includes(6)
  )
    return;
  const rect = $("board").getBoundingClientRect();
  const x = Math.floor(((e.clientX - rect.left) / rect.width) * 64),
    y = Math.floor(((e.clientY - rect.top) / rect.height) * 64);
  if (x >= 0 && x < 64 && y >= 0 && y < 64)
    perform("action", { action_id: 6, data: { x, y } });
});
document.addEventListener("keydown", (e) => {
  if (
    $("player").hidden ||
    e.target.closest("input,select,summary,button") ||
    e.ctrlKey ||
    e.metaKey ||
    e.altKey
  )
    return;
  const action = keys[e.code];
  if (!action || !state.observation?.available_actions.includes(action)) return;
  e.preventDefault();
  if (!e.repeat) perform("action", { action_id: action, data: {} });
});
window.addEventListener("pagehide", () => {
  if (window.arc3Transport) {
    window.arc3Transport.close();
    return;
  }
  if (state.session)
    fetch(`/api/sessions/${state.session}`, {
      method: "DELETE",
      keepalive: true,
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": state.csrf,
      },
      body: "{}",
    }).catch(() => {});
});
(async () => {
  try {
    state.csrf = (await api("/api/bootstrap")).csrf_token;
    state.games = await api("/api/games");
    renderGallery();
  } catch (e) {
    notice(e.message);
  }
})();
