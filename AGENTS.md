# Working on ARC3 Synthetic Games

This repository contains a fixed, independently developed collection of native
ARC3-compatible games and a local browser player. Keep game IDs and versions
stable; any mechanics change needs a new version and updated checksums.

- Keep the native environment directory usable with the official ARC3 SDK.
- Never commit credentials, personal information, raw gameplay journals or user data.
- Descriptions and the default player should support discovery; show mechanics
  explanations and demonstrations only on request.
- Execute native-code validation in an isolated development/CI environment.
  The supported end-user player is a local Python application, not a sandbox.
- Keep documentation, previews, catalog and package contents consistent.
- Do not claim official benchmark status, human baselines or complete human review.
