"use strict";
// Only the browser preview uses this transport. The local player keeps its API.
(() => {
  const catalog = fetch(new URL("catalog.json", document.baseURI)).then((r) => {
    if (!r.ok) throw new Error("The game catalog could not be loaded.");
    return r.json();
  });
  let worker = null;
  let nextId = 0;
  const pending = new Map();
  function close(message = "The game engine was stopped. Choose Play to reload it.") {
    worker?.terminate();
    worker = null;
    for (const { reject, timer } of pending.values()) {
      clearTimeout(timer);
      reject(new Error(message));
    }
    pending.clear();
  }
  function rpc(path, method, body) {
    if (!worker) {
      worker = new Worker(new URL("browser/worker.mjs", document.baseURI), { type: "module" });
      worker.onmessage = ({ data }) => {
        if (data.progress) {
          const notice = document.getElementById("notice");
          notice.textContent = data.progress;
          notice.hidden = false;
          return;
        }
        const task = pending.get(data.id);
        if (!task) return;
        pending.delete(data.id);
        clearTimeout(task.timer);
        if (data.error) {
          task.reject(new Error(data.error));
          if (data.fatal) close(data.error);
        }
        else task.resolve(data.result);
      };
      worker.onerror = () => close("The browser game engine could not load. Check your connection and try again.");
    }
    return new Promise((resolve, reject) => {
      const id = ++nextId;
      const timer = setTimeout(() => close("The game engine timed out. Choose Play to try again."), 180000);
      pending.set(id, { resolve, reject, timer });
      worker.postMessage({ id, path, method, body: body || {} });
    });
  }
  window.arc3Transport = {
    async request(path, method = "GET", body) {
      const data = await catalog;
      if (method === "GET" && path === "/api/bootstrap")
        return { csrf_token: "browser-only", version: data.version };
      if (method === "GET" && path === "/api/games")
        return data.games.map(({ mechanics, ...game }) => game);
      if (method === "GET" && /^\/api\/games\/sg\d\d\/mechanics$/.test(path)) {
        const game = data.games.find((g) => g.id === path.split("/")[3]);
        if (!game) throw new Error("Unknown game.");
        return { text: game.mechanics };
      }
      const result = await rpc(path, method, body);
      document.getElementById("notice").hidden = true;
      return result;
    },
    close,
  };
})();
