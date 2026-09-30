// Run the unchanged Python games in a dedicated WebAssembly worker.
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs";

let runtime;
let initialized = false;
async function verifiedFile(path, expected) {
  const response = await fetch(new URL(path, import.meta.url));
  if (!response.ok) throw new Error("A game runtime file could not be downloaded.");
  const bytes = await response.arrayBuffer();
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  const actual = [...new Uint8Array(digest)].map((v) => v.toString(16).padStart(2, "0")).join("");
  if (actual !== expected) throw new Error("Game runtime checksum mismatch.");
  return bytes;
}
async function initialize() {
  self.postMessage({ progress: "Loading the browser game engine… The first visit may take a minute." });
  const response = await fetch(new URL("runtime.json", import.meta.url));
  if (!response.ok) throw new Error("The game runtime manifest could not be loaded.");
  const manifest = await response.json();
  const pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/" });
  await pyodide.loadPackage(["numpy", "pydantic"]);
  for (const file of manifest.files) {
    const bytes = await verifiedFile(file.path, file.sha256);
    pyodide.unpackArchive(bytes, "zip", { extractDir: "/runtime" });
  }
  pyodide.runPython("import sys; sys.path.insert(0, '/runtime'); import browser_bridge");
  initialized = true;
  return pyodide;
}
let queue = Promise.resolve();
self.onmessage = ({ data }) => {
  queue = queue.then(async () => {
    try {
      runtime ||= initialize();
      const pyodide = await runtime;
      pyodide.globals.set("browser_request", JSON.stringify(data));
      let result;
      try {
        result = JSON.parse(pyodide.runPython("browser_bridge.request(browser_request)"));
      } finally {
        pyodide.globals.delete("browser_request");
      }
      self.postMessage({ id: data.id, result });
    } catch (error) {
      self.postMessage({ id: data.id, fatal: !initialized, error: error.message || "The game could not be loaded." });
    }
  });
};
