# Publication audit — 2026-09-30

## Assessment

The current source tree is suitable for an initial public release as an
experimental, AI-assisted collection. No credential leak, personal-data leak,
incompatible vendored license or failing native compatibility test was detected.
The main remaining publication task is to include the updated documentation and
license notices in a new release. The existing v1.0.0 tag and downloads should
remain immutable.

This audit covers the 30 native versions in the v1.0.0 catalog, the original
release packages, and the documentation/packaging changes described below.
The native source, metadata, IDs and checksums were unchanged by the audit.

## Findings and priorities

| Priority | Finding | Status or next action |
| --- | --- | --- |
| Before publication | The v1.0.0 downloads predate the expanded AI disclosure and license notices. | Issue a new documentation/package release, for example v1.0.1; retain all native game versions and hashes. Do not silently replace v1.0.0 assets. |
| Corrected | The third-party notice said upstream license files were present in the installed ARC distributions; the tested wheels contained license declarations but no standalone license files. | Reproduced both upstream MIT notices in `THIRD_PARTY_NOTICES.md` and included that file in the built wheel. |
| Corrected | The README lacked a prominent AI disclosure. | Added an AI disclosure at the bottom, including the distinction between AI-assisted development and genuine human GIF demonstrations. |
| Research limitation | Public tests initialize and step all 210 levels but do not solve every level to completion. | Add independent winning replays or solver checks before claiming universal solvability. Current documentation already states this limitation. |
| Research limitation | Population difficulty, blind human discoverability and official human-efficiency baselines are unmeasured. | Keep the experimental-dataset wording. Technical passes do not establish these properties. |
| Optional improvement | Automated UI tests are not part of the committed CI suite; the prior browser check is documented separately. | Add a small browser smoke test if the player changes. Current API/native tests passed. |
| Deployment boundary | The player executes curated Python locally and is not a public hosting service or arbitrary-code sandbox. | Preserve the documented loopback-only launch and supported Python 3.12 runtime. |

## Privacy and secrets

- Scanned all 125 files tracked at the audit baseline and all reachable Git
  history: one commit, 125 distinct file blobs, and neutral author/committer
  identities using a non-deliverable placeholder address.
- Gitleaks 8.30.1 found no secrets in history, the staged source tree, the three
  original downloadable packages or the fresh wheel/source distribution.
  Its downloaded executable was checked against the upstream SHA-256 manifest;
  scanner reports were redacted.
- Additional scans found no personal names, real email addresses, local user
  paths, provider tokens or private keys in the checked content. No raw gameplay
  journals, databases, credentials, official game packages, bytecode caches or
  development virtual environments were present in the release archives.
- Inspected all 37 media assets: 31 PNGs and six GIFs. No PNG text/EXIF/time
  metadata, GIF comment/text records or trailing hidden data were found.
  Inspected the representative overview visually; the distributed media shows
  game boards rather than desktop or browser captures.
- A public repository hosted under a personal GitHub account still exposes that
  account and profile through GitHub. Neutral file contents and commit identities
  do not make the hosting account anonymous.

These checks are scoped detection results, not a guarantee that every possible
secret encoding or identifying pattern can be recognized.

## Technical evidence

- Catalog inventory: exactly SG01–SG30, 210 levels and 60 native files. Identities,
  SHA-256 hashes and referenced media matched.
- All native Python parsed successfully without execution on the host. Imports
  were limited to NumPy, the ARC engine, `collections`, `math` and future
  annotations. No direct native calls to `exec`, `eval`, `open`, `compile` or
  `__import__` were found.
- The source test suite passed **69 tests** in an isolated Docker runtime.
  A freshly built and installed wheel passed the same **69 tests** from outside
  the source checkout, plus the module's data-only `verify` command.
- Native execution used a fixed image ID, no network, an unprivileged user,
  read-only mounts/root filesystem, dropped capabilities, no-new-privileges and
  memory/CPU/PID limits. No home directory, credentials or private human journals
  were mounted.
- Both fresh wheel and source distribution built successfully on Windows.
  Each contained exactly the same 60 native files, the project license, the
  expanded third-party notices and the AI disclosure. Neither contained
  identifying paths, bytecode caches or private runtime data.
- All three original release package hashes matched `SHA256SUMS.txt`; their
  native files matched the catalog. Those assets retain their original docs.
- Ruff passed for the player and tests. `CITATION.cff` passed the official CFF
  1.2.0 schema through `cffconvert`; relative Markdown links resolved.
- `pip-audit` checked all **37 resolved runtime dependencies**, with no skipped
  packages and **zero reported known vulnerabilities** on the audit date.
  TLS verification remained enabled; the Windows system trust store resolved a
  local certificate-chain issue. This result is time-bound.
- The test client emits a Starlette/HTTPX deprecation warning. It does not affect
  the passing checks; a future test-transport update can address it.

The local request boundary, allowed game IDs, strict action validation,
independent sessions, resets, optional mechanics reveals and absence of recording
endpoints are covered by the committed tests. The application contains no remote
analytics scripts or game-code upload endpoint. CI uses read-only repository
permissions and disables persisted checkout credentials.

## Licensing and provenance

The project's MIT license covers the original games, player, documentation and
presentation assets. The ARC engine and SDK are external MIT dependencies;
their full upstream notices and links are now retained in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Other dependencies keep their
own licenses, including Certifi's MPL-2.0; they are installed separately rather
than relicensed or vendored by this project.

Compared all 30 native sources with the 25 official Python environment files
in the supplied reference archive. No exact source copies or common consecutive
blocks of 15 or more lines were found. This checks that archive, not every code
repository or third-party work; it does not prove global originality or eliminate
all potential intellectual-property claims.

OpenAI's [European terms](https://openai.com/policies/eu-terms-of-use/) assign its
rights in outputs to the user to the extent permitted by law, while excluding
other users' and third-party outputs. The
[service terms for Codex/code generation](https://openai.com/policies/service-terms/)
also state that generated code can carry third-party licenses. AI-assisted
authorship therefore does not by itself prevent an MIT release, but the MIT
label and AI disclosure do not establish originality or copyright protection
for every generated element.

The README and dataset card appropriately identify an independent synthetic
collection, distinguish demonstrations from trajectory data, and avoid claims
of ARC Prize endorsement, official scores or complete human approval.
