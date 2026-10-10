# Packages and hosting

The playable Studio collection and source-informed AI data have separate package
scopes. Installing the player or opening the browser demo does not download
NVIDIA source or trajectory data.

## Release artifacts

| Artifact | Contents |
| --- | --- |
| `environments.zip` | 50 Studio native games, catalog, previews, human GIF excerpts and native documentation |
| `source.zip` | Tracked public source: player, three AI-data partitions, attributed NVIDIA packages, analysis and documentation |
| `browser-preview.zip` | Static player for 50 Studio games, without NVIDIA code or trajectory recordings |
| `.whl` / `.tar.gz` | Installable 50-game Studio player; excludes AI datasets, NVIDIA code and agent demo assets |
| `agent-trajectories.zip` | Three compressed AI-data partitions, native records, manifests, statistics and licenses; no game code or raw human trajectories |
| `dataset.zip` | All 75 environments, NVIDIA support, AI data, licenses and standard-library loader; no player, GIFs or generation setup |
| `SHA256SUMS.txt` | SHA-256 hashes of release assets; data archives also contain their own inventories |

Artifacts are immutable and identified by a version and Git tag.
Version 2.0.0's combined agent dataset ID is
`arc3-source-informed-agent-v2.0.0`; earlier partition IDs remain unchanged.
Catalogs and manifests bind exact environment versions.

## Build archives

```bash
python tools/build_trajectory_release.py --output dist/arc3-synthetic-games-v2.0.0-agent-trajectories.zip
```

This data-only builder verifies inventories and licenses without executing game
code. It requires a new output path.

`tools/build_release.py` requires a clean committed source tree, matching browser
preview and built Python packages. It creates source, native, browser, Python,
trajectory and complete-dataset assets with checksums.

## Browser hosting

The browser demo runs the same 50 Studio Python sources through Pyodide 314.0.7.
A modern browser with WebAssembly and module-worker support is required.
The first runtime download needs internet; local Python play remains available
offline after installation.

For GitHub Pages, choose **GitHub Actions** in **Settings → Pages → Build and
deployment**, then run **Browser demo**. A push to `main` also triggers the
workflow. The deployment URL is
<https://felix561.github.io/arc3-synthetic-games/>.
The workflow builds private repositories too, but deploys only when public.
It uses GitHub's scoped workflow token; no personal deployment token belongs
in the repository.

The static build also includes the independently authored statistical report at
`analysis/`. It copies only the hash-verified inventory in
`docs/analysis/manifest.json`; unlisted files or changed assets fail the build.
The report also opens directly as an offline HTML file. Its sources, aggregate
data and license are documented in [the analysis guide](analysis/README.md).
The report does not change the frozen environment or trajectory release.

For another static host, run `python tools/build_preview.py` and serve `_site/`
over HTTPS. The playable demo requires HTTP(S); the analysis report also works
from `file://`. No backend is needed.
Engine and game downloads are SHA-256 checked before loading; checksums establish
artifact consistency, not hosting-provider trust.

Browser gameplay stays in memory, creates no trajectories and includes no
analytics. GitHub Pages and the runtime CDN receive ordinary asset requests.
Agent GIFs and downloadable data are separate static assets.
