# Publishing and release packages

## GitHub Pages

The browser demo plays all 30 native games without installing Python. It uses
Pyodide 314.0.7 in a WebAssembly worker and the same game files as the dataset.
Runtime downloads require an internet connection and a modern browser with
WebAssembly and module-worker support. Tested browsers are listed in
[VALIDATION.md](VALIDATION.md). Local Python play remains available offline.

To publish this repository and enable its demo:

1. Make the repository public when ready.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. In **Actions → Browser demo**, run the workflow (or push a commit to `main`).

The deployment URL is `https://felix561.github.io/arc3-synthetic-games/`.
The workflow builds on private repositories too, but only deploys when public.
No deployment token or personal credential belongs in the repository. The
one-time Pages setting requires a repository administrator; the workflow's
normal GitHub token cannot enable a previously unconfigured Pages site.

For another static host, build with `python tools/build_preview.py`, then serve
the `_site/` contents over HTTPS. Do not open `index.html` through `file://`.
No backend is needed. The engine wheel and game archive are checked against
SHA-256 hashes before loading. This protects artifact consistency, not against
a compromised hosting provider or CDN.

Browser gameplay stays in memory and does not create trajectories or completion
receipts. No analytics are included. GitHub Pages and jsDelivr serve web requests
and may retain request information under their own policies.

## Packages

- **environments.zip:** Native games, catalog, previews and dataset documentation.
  Use directly with the offline ARC3 SDK.
- **source.zip:** Complete tracked source, local player, browser build tools and tests.
- **browser-preview.zip:** Built static site for an HTTPS/static host.
- **.whl / .tar.gz:** Installable Python package and source distribution.
- **SHA256SUMS.txt:** Checksums for the five artifacts above.

Release 1.0.2 keeps every native game ID, version and source/metadata hash from
1.0.0. Only packaging, player transport, browser hosting and documentation change.
Previous release tags and assets remain available unchanged.
