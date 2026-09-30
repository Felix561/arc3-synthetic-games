# Third-party acknowledgments

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
