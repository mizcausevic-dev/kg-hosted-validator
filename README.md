# kg-hosted-validator

The single-file static web app behind **[validator.kineticgain.com](https://validator.kineticgain.com/)**. Paste any Kinetic Gain Protocol Suite JSON document and get a procurement-grade validation report. Everything runs in the browser — no upload, no server, no signup.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## What it does

1. You paste a JSON document into the textarea.
2. The page detects which Suite spec it belongs to via the top-level version field (`aeo_version`, `clinical_ai_card_version`, `aup_version`, …).
3. It validates the document against the bundled JSON Schema 2020-12 document for that spec.
4. The result panel shows pass/fail, the detected spec, the count of schema errors, and a per-error path + message list.

All ten spec schemas are bundled into `index.html` at build time. The ajv validator is loaded over HTTPS from `esm.sh` at runtime (no `npm install`, no bundler).

## Architecture

- **One file:** `index.html` (~96 KB). Contains markup, CSS, the schema bundle, the example bundle, and the JS that runs everything.
- **AJV via ESM CDN:** `<script type="importmap">` maps `ajv` and `ajv-formats` to `esm.sh`. The module script imports `Ajv2020` and compiles each bundled schema once at page load.
- **No build step:** the file is shipped as-is. To update schemas, run `make.py` (or the equivalent shell flow in `build.sh`) to regenerate `index.html` from the latest spec-repo schemas + examples.

## Local development

```bash
# Serve over plain HTTP so import maps + ESM work
python -m http.server 8765 --bind 127.0.0.1
# Then open http://127.0.0.1:8765/
```

Editing `index.html` and refreshing is enough — there's no compile or bundle step.

## Rebuilding the schemas / examples bundle

The `index.html` file embeds two JSON blobs:

- `schemas-blob`: the 10 spec schemas, keyed by short name (`aeo`, `clinical-ai-card`, …).
- `examples-blob`: one canonical example per spec, used by the "Try an example" pills.

When upstream specs change, regenerate these blobs from the spec repos and re-substitute into the template. See `build.md` for the exact reproducible recipe.

## Deploy

The single `index.html` file deploys cleanly to any static host. The production target is **`validator.kineticgain.com`** on Hostinger via FTP, matching the rest of the Kinetic Gain Suite property fleet.

## License

MIT. The schemas this validator ships with are also MIT (from their respective spec repos under [github.com/mizcausevic-dev](https://github.com/mizcausevic-dev)). The same dual-license stance as the rest of the Suite: specs and consumer SDKs are MIT, reference implementations like `mcp-kinetic-gain` are AGPL-3.0.

## Related

- **Suite hub:** [suite.kineticgain.com](https://suite.kineticgain.com/)
- **MCP server + CLI:** [`mcp-kinetic-gain`](https://github.com/mizcausevic-dev/mcp-kinetic-gain) — same validation logic, but as an installable npm package with both a stdio MCP server and a `validate` CLI subcommand
- **GitHub Action:** [`kg-validate-action`](https://github.com/mizcausevic-dev/kg-validate-action) — drop-in CI workflow for vendor repos
- **Apex:** [kineticgain.com](https://kineticgain.com/)
