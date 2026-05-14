#!/usr/bin/env python3
"""
Rebuild index.html from template + spec repos.

Inputs (paths relative to the parent directory of this repo):
  ../<spec-repo>/<name>.schema.json   # JSON Schema 2020-12 per spec
  ../<spec-repo>/examples/*.json      # one or more canonical examples per spec

Output:
  index.html                          # single-file static app, ready to deploy

Run from this repo's root:
  python build.py
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent

# (short_key, spec_repo, schema_filename, example_basename)
SPECS = [
    ("aeo",                   "aeo-protocol-spec",          "aeo.schema.json",                  "aeo-organization.json"),
    ("provenance",            "prompt-provenance-spec",     "provenance.schema.json",           "deprecated-version.json"),
    ("agent-card",            "agent-cards-spec",           "agent-card.schema.json",           "customer-support-agent.json"),
    ("evidence",              "ai-evidence-format-spec",    "evidence.schema.json",             "background-citation.json"),
    ("tool-card",             "mcp-tool-card-spec",         "tool-card.schema.json",            "admin-reset.json"),
    ("tutor-card",            "ai-tutor-card-spec",         "tutor-card.schema.json",           "college-cs-assistant.json"),
    ("student-ai-disclosure", "student-ai-disclosure-spec", "student-ai-disclosure.schema.json", "ai-edit-hashed-prompts.json"),
    ("aup",                   "classroom-ai-aup-spec",      "aup.schema.json",                  "district-k12-strict.json"),
    ("clinical-ai-card",      "clinical-ai-disclosure-spec", "clinical-ai-card.schema.json",    "research-molecule-design.json"),
    ("incident-card",         "ai-incident-card-spec",      "incident-card.schema.json",        "pii-leak-cite-check.json"),
    ("decision-card",         "ai-procurement-decision-spec","decision-card.schema.json",       "district-edtech-approved-conditions.json"),
]

DISPLAY_NAMES = {
    "aeo":                   "AEO Protocol",
    "provenance":            "Prompt Provenance",
    "agent-card":            "Agent Card",
    "evidence":              "AI Evidence Format",
    "tool-card":             "MCP Tool Card",
    "tutor-card":            "AI Tutor Card",
    "student-ai-disclosure": "Student AI Disclosure",
    "aup":                   "Classroom AI AUP",
    "clinical-ai-card":      "Clinical AI Card",
    "incident-card":         "AI Incident Card",
    "decision-card":         "AI Procurement Decision Card",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    template_path = HERE / "template.html"
    out_path = HERE / "index.html"

    if not template_path.exists():
        print(f"error: {template_path} not found", file=sys.stderr)
        return 1

    schemas = {}
    examples = {}
    missing = []

    for key, repo, schema_name, example_name in SPECS:
        schema_path = PARENT / repo / schema_name
        example_path = PARENT / repo / "examples" / example_name
        if not schema_path.exists():
            missing.append(str(schema_path))
            continue
        if not example_path.exists():
            missing.append(str(example_path))
            continue
        schemas[key] = load_json(schema_path)
        examples[key] = {
            "label": DISPLAY_NAMES[key],
            "doc": load_json(example_path),
        }

    if missing:
        print("error: missing input files:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 1

    template = template_path.read_text(encoding="utf-8")
    html = (
        template
        .replace("__SCHEMAS_PLACEHOLDER__", json.dumps(schemas, separators=(",", ":")))
        .replace("__EXAMPLES_PLACEHOLDER__", json.dumps(examples, separators=(",", ":")))
    )
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path}: {out_path.stat().st_size} bytes")
    print(f"  schemas:  {len(schemas)} embedded")
    print(f"  examples: {len(examples)} embedded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
