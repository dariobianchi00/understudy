#!/usr/bin/env python3
"""Create a run folder and its manifest.

Phase-gate check 5 requires a complete manifest. Writing it at run start —
rather than reconstructing it at the end — is what makes that check meaningful:
a manifest assembled afterwards records what someone remembers, not what ran.

Usage:
    init_run.py --target ~/.understudy/targets/<slug>.yaml \\
                --traversal-model <name> \\
                [--run-id <id>] [--output-dir <path>]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone


def load_target(path):
    """Read the target file. Uses PyYAML when present, else a narrow fallback
    parser covering the subset of YAML the target schema actually uses."""
    text = open(os.path.expanduser(path)).read()
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return _minimal_yaml(text)


def _minimal_yaml(text):
    """Fallback for the target schema only. Handles what the schema uses:
    scalars, nested mappings, and '- ' lists of scalars or of one-level
    mappings. Not a general YAML parser and does not pretend to be —
    install PyYAML if the target file grows beyond this."""
    root = {}
    # stack of (indent, container); container is a dict being filled
    stack = [(-1, root)]
    current_list = None      # list being appended to, if any
    list_indent = None
    list_item = None         # dict for the current '- key: value' item

    for raw in text.split("\n"):
        line = raw.split("#")[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        # ---- list items -------------------------------------------------
        if stripped.startswith("- "):
            if current_list is None:
                continue                      # list with no owning key; skip
            body = stripped[2:].strip()
            # A mapping needs colon-SPACE. Splitting on a bare ":" turns every
            # URL in a list into {"https": "//example.test"} — which is how a
            # competitor list silently becomes nonsense.
            if ": " in body and not body.startswith(('"', "'")):
                key, _, val = body.partition(": ")
                list_item = {key.strip(): _scalar(val)}
                current_list.append(list_item)
            else:
                current_list.append(_scalar(body))
                list_item = None
            list_indent = indent
            continue

        # continuation of a '- key: value' item (deeper indent, same block)
        if list_item is not None and list_indent is not None and indent > list_indent:
            if ": " in stripped:
                key, _, val = stripped.partition(": ")
                list_item[key.strip()] = _scalar(val)
            continue

        # ---- leaving any list ------------------------------------------
        if current_list is not None and list_indent is not None and indent <= list_indent:
            current_list, list_indent, list_item = None, None, None

        if ":" not in stripped:
            continue

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]

        key, _, val = stripped.partition(":")
        key, val = key.strip(), val.strip()

        if val == "":
            # Opens either a mapping or a list — we find out on the next line.
            # Store a dict now; if list items follow, replace it with the list.
            child = {}
            container[key] = child
            stack.append((indent, child))
            current_list = _PendingList(container, key)
            list_indent, list_item = indent, None
        else:
            container[key] = _scalar(val)
            current_list, list_indent, list_item = None, None, None

    return root


class _PendingList:
    """A key opened with no inline value may become a mapping or a list.
    The first appended item settles it as a list, replacing the placeholder
    dict the parser optimistically stored."""

    def __init__(self, container, key):
        self.container, self.key, self.items = container, key, []

    def append(self, item):
        self.items.append(item)
        self.container[self.key] = self.items


def _scalar(v):
    v = v.strip()

    # Flow sequences — "[]", "[30, 60, 75]", "[a, b]". The schema uses these for
    # checkpoints and for an empty scope_exclusions, and without this they arrive
    # as the STRING "[]", which reads as one exclusion named "[]" and quietly
    # defeats the manifest's completeness check.
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_scalar(item) for item in inner.split(",")]

    v = v.strip('"').strip("'")
    if v in ("null", "~", ""):
        return None
    if v == "true":
        return True
    if v == "false":
        return False
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    p.add_argument("--traversal-model", required=True,
                   help="The SESSION model. understudy cannot set this; it records what it was told.")
    p.add_argument("--run-id", default=None)
    p.add_argument("--output-dir", default=None)
    p.add_argument("--persona-mode", default=None, choices=["generic", "supplied"])
    args = p.parse_args()

    target = load_target(args.target) or {}
    slug = target.get("slug") or "unknown"
    run_id = args.run_id or uuid.uuid4().hex[:8]
    today = datetime.now().strftime("%Y-%m-%d")

    out = args.output_dir or target.get("output_dir") or f"~/.understudy/runs/{slug}"
    run_dir = os.path.expanduser(os.path.join(out, f"{today}-run-{run_id}"))

    if os.path.realpath(run_dir).startswith(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))):
        sys.exit("REFUSED: run output would land inside the understudy repo. "
                 "Real run artifacts must never enter a public repo (see CLAUDE.md §7).")

    personas = target.get("personas") or []
    for persona in personas:
        name = persona.get("name", "persona") if isinstance(persona, dict) else str(persona)
        os.makedirs(os.path.join(run_dir, f"persona-{name}", "screenshots"), exist_ok=True)

    models = target.get("models") or {}
    manifest = {
        "run_id": run_id,
        "target_slug": slug,
        "product_name": target.get("product_name"),
        "base_url": target.get("base_url"),
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "finished_utc": None,

        # Models — recorded at BOTH levels. Findings are not comparable across
        # models; a --since diff must flag a change rather than present it silently.
        "models": {
            "traversal": args.traversal_model,
            "traversal_settable_by_understudy": False,
            "scoring": models.get("scoring") or {},
            "scoring_shape": models.get("scoring_shape"),
        },

        # Website / Phase-4 fields. Absent on an older target file, which is
        # why every consumer must treat None as "not asked", never as a default.
        "assessment_type": target.get("assessment_type"),
        "coverage_depth": target.get("coverage_depth") or "standard",
        "conversion_goal": target.get("conversion_goal"),
        "competitors": target.get("competitors") or [],
        # ⚑ Only the OBJECTIVE reaches the manifest. The success criterion is
        # split out to objectives/criteria.json, which the traversal must never
        # open — see CLAUDE.md Phase 4, O2. "Don't look" is not a mechanism when
        # the orchestrator and the persona are the same agent, so the criterion
        # is physically not in the file the traversal reads.
        "objectives_under_test": [
            {"objective": o.get("objective")} if isinstance(o, dict) else {"objective": o}
            for o in (target.get("objectives_under_test") or [])
        ],

        "persona_mode": args.persona_mode or target.get("persona_mode"),
        "personas": [
            {"name": p.get("name"), "device": p.get("device")}
            for p in personas if isinstance(p, dict)
        ],
        "objectives": target.get("objectives") or [],
        "scope_exclusions": target.get("scope_exclusions") or [],
        "time_cap_minutes": target.get("time_cap_minutes"),
        "understudy_version": _version(),
        "phase": "2a-capture",
        "captures": {},
    }

    os.makedirs(run_dir, exist_ok=True)

    # The withheld half. Written once, read only by objectives-scorer.
    objs = target.get("objectives_under_test") or []
    if objs:
        os.makedirs(os.path.join(run_dir, "objectives"), exist_ok=True)
        with open(os.path.join(run_dir, "objectives", "criteria.json"), "w") as f:
            json.dump({
                "_warning": "DO NOT OPEN DURING CAPTURE. Reading this during a "
                            "traversal guarantees the objective passes and makes "
                            "the test worthless. See CLAUDE.md Phase 4, O2.",
                "criteria": [
                    {"objective": o.get("objective"), "expected": o.get("expected")}
                    for o in objs if isinstance(o, dict)
                ],
            }, f, indent=2)
            f.write("\n")

    manifest_path = os.path.join(run_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(run_dir)
    if manifest["persona_mode"] == "generic":
        print("NOTE: persona_mode=generic — findings rest on INFERRED personas. "
              "This must appear on the face of the report.", file=sys.stderr)
    return 0


def _version():
    here = os.path.dirname(os.path.abspath(__file__))
    plugin = os.path.join(here, "..", ".claude-plugin", "plugin.json")
    try:
        return json.load(open(plugin)).get("version")
    except Exception:
        return None


if __name__ == "__main__":
    sys.exit(main())
