# Third-party acknowledgments

## Statistical analysis report

The report under `docs/analysis/` uses original project-authored HTML, CSS,
JavaScript and independently drawn statistical graphics, under the report's
MIT notice. It bundles no third-party report runtime, JavaScript libraries,
fonts, official environment code or official game images. Official-human
comparisons contain derived aggregate statistics with source citations, not
individual human replay paths. Original upstream game/data rights remain with
their respective sources; the report's license does not relicense them.
Figure generation uses Matplotlib as a development tool; no Matplotlib code or
font binary is included in the report. ARC Prize and NVIDIA do not endorse
the analysis. Dataset-specific upstream notices below remain applicable.

## Studio V2 design references

The V201–V220 games are independently implemented Studio environments. Their
separation of state, rendering and transition functions was informed by
[NVIDIA DreamTeam's game-creation structure](https://github.com/NVIDIA/dream-team/tree/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9/arc_agi_3).
Public ARC3 games also informed abstract design choices. These references are
acknowledgments of inspiration; no official ARC Prize game files are included.
Studio V2 source, agent data and its presentation assets use the project's MIT
license. The separate NVIDIA subtree retains its own licenses and notices.

## NVIDIA DreamTeam synthetic environments and derived agent data

Source: [NVIDIA/dream-team](https://github.com/NVIDIA/dream-team), pinned to
[`bffef22f3e50fb7dcd6b2dc20005e6986e1479e9`](https://github.com/NVIDIA/dream-team/tree/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9).

Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
The 25 generated native game modules and included runtime adapter declare
`SPDX-License-Identifier: Apache-2.0`.

The repository separately includes unchanged NVIDIA game packages/support under
`third_party/nvidia/`, recordings under `trajectories/nvidia/`, and derived GIFs
in `media/agent-demos/nvidia/`. NVIDIA-based recordings and renderings
are distributed with Apache-2.0 attribution. Original Studio content remains MIT;
the root MIT license does not replace upstream rights.

Full license/notice texts are retained in the NVIDIA subtree and included in
the standalone trajectory archive:

- [Pinned LICENSE](https://github.com/NVIDIA/dream-team/blob/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9/LICENSE), including applicable MIT third-party terms.
- [Pinned NOTICE](https://github.com/NVIDIA/dream-team/blob/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9/NOTICE).
- [Pinned THIRD_PARTY_NOTICES](https://github.com/NVIDIA/dream-team/blob/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9/THIRD_PARTY_NOTICES).

NVIDIA's NOTICE reads:

```text
DreamTeam
Copyright 2026 NVIDIA Corporation

This product includes software developed by NVIDIA Corporation.

Portions of this distribution incorporate or are adapted from BeamDS,
FastChat, and Deep Agents. Their applicable copyright and license notices
are reproduced in THIRD_PARTY_NOTICES.
```

The Studio player/browser/wheel packages do not include the NVIDIA game tree or
agent trajectory data. Combined statistics/graphics are original project
analysis; NVIDIA-derived game pixels retain the source's attribution.
NVIDIA and ARC Prize do not endorse this independently maintained dataset.

## Studio player dependencies

This independent collection uses the ARC Prize Foundation's ARC engine and
[ARC-AGI toolkit](https://github.com/arcprize/ARC-AGI), pinned as `arcengine==0.9.3`
and `arc-agi==0.9.8`. Both installed distributions identify their license as MIT.
The local player installs them as dependencies. The built browser demo bundles
the unmodified arcengine 0.9.3 wheel, preserving its package metadata and the
full MIT notice below. No official game packages are distributed.
Their license declarations are present in package metadata. The tested wheels
do not include standalone license files, so the upstream MIT notices are
reproduced below. These notices also acknowledge the engine's palette convention.

The local player also depends on NumPy (BSD-3-Clause, with additional bundled
component notices), FastAPI (MIT), Uvicorn (BSD-3-Clause) and their dependencies.
Transitive dependencies include packages under MIT, BSD, Apache, PSF and MPL-2.0
licenses. For example, Requests uses Apache-2.0 and Certifi uses MPL-2.0. These
packages are installed separately; their licenses apply to those packages and
are not replaced by this repository's MIT license. Bundling dependency binaries
or modified dependency source requires preserving their corresponding notices
and satisfying those licenses.

Original native games, player code, catalog prose, previews and anonymous
gameplay GIF assets in this repository are covered by the project's MIT license.
The 16-color palette and native game interface follow the ARC3 engine convention.

## Browser runtime

The browser demo loads unmodified [Pyodide 314.0.7](https://github.com/pyodide/pyodide)
and its NumPy/Pydantic packages from jsDelivr. Pyodide's own code is under
[MPL-2.0](https://github.com/pyodide/pyodide/blob/314.0.7/LICENSE); its source and
license remain available at that versioned repository. CPython, NumPy, Pydantic
and their bundled components retain their upstream licenses. These runtime
files are served by the CDN, not included in the source repository or Python
wheel. This project's browser adapter is separate MIT-licensed code; it does
not modify or relicense Pyodide or its dependencies.

## ARC engine

Source: [arcprize/ARCEngine license](https://github.com/arcprize/ARCEngine/blob/main/LICENSE).
The following upstream notice was checked on 2026-09-30.

```text
MIT License

Copyright (c) 2026 ARC Prize Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ARC-AGI toolkit

Source: [arcprize/ARC-AGI license](https://github.com/arcprize/ARC-AGI/blob/main/LICENSE).
The copyright line below reproduces the upstream wording exactly; it was
checked on 2026-09-30.

```text
MIT License

Copyright (c) 2026 ARC Prize 2026 ARC Prize Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
