# Packages and hosting

The playable Studio collection and the source-informed AI trajectory datasets
are separate deliverables. Installing the player or opening its browser demo
does not download NVIDIA game code or trajectory data.

## Package contents

| Artifact | Contents |
| --- | --- |
| `environments.zip` | The 30 Studio native games, catalog, previews, human gameplay GIF excerpts and native documentation. |
| `source.zip` | Complete tracked public source, including the player, both trajectory partitions, separately licensed NVIDIA environments, analysis and documentation. |
| `browser-preview.zip` | A static player for the 30 Studio games. It contains no NVIDIA environment code or trajectory recordings. |
| `.whl` / `.tar.gz` | The installable 30-game Studio player. Large trajectory datasets, NVIDIA code and agent demonstration assets are excluded. |
| `agent-trajectories.zip` | Data-only Studio and NVIDIA partitions: compressed canonical rows, native recordings, manifests, statistics and relevant licenses/notices. No game Python, player or raw human trajectories. |
| `dataset.zip` | All 55 exact synthetic environments, NVIDIA runtime support, both agent-data partitions, licenses, loading guide and dependency-free streaming loader. No player, GIFs or generation setup. |
| `SHA256SUMS.txt` | SHA-256 checksums for the release artifacts. The trajectory ZIP also contains checksums for its own data, docs and licenses. |

Release artifacts are immutable and identified by a project version and Git tag.
The trajectory dataset has its own version, `arc3-source-informed-agent-20261002-v1`.
Native environment IDs and hashes are recorded in the catalog and dataset manifests.
See [TRAJECTORIES.md](TRAJECTORIES.md) for source-informed agent provenance and
[STATISTICS.md](STATISTICS.md) for observed outcomes. These are AI recordings,
not human gameplay or blind benchmark results.

## Prepare a local trajectory archive

Build a data-only archive:

```bash
python tools/build_trajectory_release.py --output dist/arc3-source-informed-agent-20261002-v1.zip
```

The builder verifies file checksums and partition licenses, then writes a
deterministic ZIP without executing game code. The output path must not exist.

`tools/build_release.py` requires a clean, committed source tree, a matching browser
preview and built Python packages. It creates source, native, browser, Python,
trajectory and complete-dataset artifacts with a release checksum inventory.
Upload the resulting files to the matching GitHub release.

## Browser hosting

The browser demo plays all 30 native Studio games without installing Python.
It uses Pyodide 314.0.7 in a WebAssembly worker and the same Studio game files
as the dataset. Runtime downloads require an internet connection and a modern
browser with WebAssembly and module-worker support. Tested browsers are listed
in [VALIDATION.md](VALIDATION.md). Local Python play remains available offline.

For GitHub Pages, select **GitHub Actions** in **Settings → Pages → Build and
deployment**, then run the **Browser demo** workflow. A push to
`main` also triggers that workflow. The deployment URL for this repository is
<https://felix561.github.io/arc3-synthetic-games/>. The workflow builds on private
repositories too, but only deploys when public. No personal deployment token
belongs in the repository; it uses GitHub's scoped workflow token.

For another static host, run `python tools/build_preview.py`, then serve the
`_site/` contents over HTTPS. Do not open `index.html` through `file://`. No
backend is needed. Engine and game downloads are checked against SHA-256 hashes
before loading; this checks artifact consistency, not hosting-provider trust.

Browser gameplay stays in memory and creates no trajectories or completion
receipts. No analytics are included. GitHub Pages and jsDelivr handle ordinary
web requests under their own policies. Agent GIFs and downloadable trajectories
are separate static research assets; the live browser demo does not record them.
