#!/usr/bin/env python3
"""What a run folder looks like on disk — shared by the gates, the renderer and
the differ, so all three agree on which folders are lenses and which site a
lens belongs to.

Why this file exists: observed 2026-09-11, `check_report.py` listed lens
folders one level deep, `render_report.py` recursed into `compare/<site>/`,
and `compare_runs.py` did neither consistently. A Mode D run therefore had
three per-site reports the gate never saw and the renderer averaged into the
client's own score. Three copies of "where do lenses live" were three
different answers.

Stdlib only, like every script here.
"""
import json
import os


def _read(*a, **k):
    with open(*a, **k) as fh:
        return fh.read()


def _write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


LENS_FILE = "findings-final.md"


def lens_dirs(run):
    """Every folder holding a findings-final.md, relative to the run root.

    Mode D nests lenses one level deeper under `compare/<site>/<lens>/`, and
    `compare/` itself is a lens (the diff pass). A flat scan misses every
    per-site report; a scan that stops at the first findings-final.md drops
    them silently. This walks both.
    """
    found = []

    def walk(base, prefix=""):
        if not os.path.isdir(base):
            return
        for d in sorted(os.listdir(base)):
            full = os.path.join(base, d)
            if not os.path.isdir(full) or d.startswith((".", "_")):
                continue
            if os.path.exists(os.path.join(full, LENS_FILE)):
                found.append(prefix + d)
            if d == "compare" or prefix:
                walk(full, f"{prefix}{d}/")

    walk(run)
    return found


def compare_sites(run):
    """`compare/<site>/` folders, relative to the run root."""
    base = os.path.join(run, "compare")
    if not os.path.isdir(base):
        return []
    return [f"compare/{d}" for d in sorted(os.listdir(base))
            if os.path.isdir(os.path.join(base, d)) and not d.startswith(".")]


def site_of(lens_dir):
    """`compare/<site>/<lens>` -> `compare/<site>`; anything else -> None."""
    parts = lens_dir.split("/")
    if len(parts) == 3 and parts[0] == "compare":
        return "/".join(parts[:2])
    return None


def _norm_url(u):
    u = (u or "").strip().lower().rstrip("/")
    for p in ("https://", "http://"):
        if u.startswith(p):
            u = u[len(p):]
    return u[4:] if u.startswith("www.") else u


def site_roles(run, manifest=None):
    """Which `compare/<site>` is the client's own site, and which are competitors.

    Resolution order, most explicit first:
      1. `compare/index.json` -> sites[].role == "ours" | "competitor"
      2. the site's url matches the manifest's base_url
      3. the slug starts with `ours-`
      4. otherwise, competitor

    Returns {"compare/<site>": "ours" | "competitor"}. The client's score is
    the mean of *their* lenses; a competitor scored 10/10 must never lift it.
    """
    roles = {}
    sites = compare_sites(run)
    if not sites:
        return roles

    if manifest is None:
        try:
            manifest = json.loads(_read(os.path.join(run, "manifest.json")))
        except (OSError, ValueError):
            manifest = {}
    base_url = _norm_url(manifest.get("base_url"))

    index = {}
    try:
        idx = json.loads(_read(os.path.join(run, "compare", "index.json")))
        for s in idx.get("sites") or []:
            if isinstance(s, dict) and s.get("slug"):
                index[s["slug"]] = s
    except (OSError, ValueError):
        pass

    for site in sites:
        slug = site.split("/", 1)[1]
        rec = index.get(slug, {})
        role = rec.get("role")
        if role not in ("ours", "competitor"):
            if base_url and _norm_url(rec.get("url")) == base_url:
                role = "ours"
            elif slug.startswith("ours-"):
                role = "ours"
            else:
                role = "competitor"
        roles[site] = role
    return roles


def is_ours(lens_dir, roles):
    """True for the client's own lenses — root-level, the compare diff lens,
    and per-site lenses under the site marked ours."""
    site = site_of(lens_dir)
    if site is None:
        return True
    return roles.get(site) == "ours"


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        for d in ("clarity", "compare", "compare/ours-x/clarity",
                  "compare/comp-a/clarity", "compare/comp-a/trust",
                  "persona-p", "crawl"):
            os.makedirs(os.path.join(t, d), exist_ok=True)
        for d in ("clarity", "compare", "compare/ours-x/clarity",
                  "compare/comp-a/clarity", "compare/comp-a/trust"):
            _write(os.path.join(t, d, LENS_FILE), "## Findings\n")
        got = lens_dirs(t)
        assert got == ["clarity", "compare", "compare/comp-a/clarity",
                       "compare/comp-a/trust", "compare/ours-x/clarity"], got
        assert compare_sites(t) == ["compare/comp-a", "compare/ours-x"]
        assert site_of("compare/comp-a/trust") == "compare/comp-a"
        assert site_of("clarity") is None and site_of("compare") is None

        # slug prefix fallback
        roles = site_roles(t, manifest={})
        assert roles == {"compare/comp-a": "competitor", "compare/ours-x": "ours"}, roles
        # manifest base_url beats the prefix
        os.makedirs(os.path.join(t, "compare", "comp-b"))
        json.dump({"sites": [{"slug": "comp-b", "url": "https://www.Client.test/"}]},
                  open(os.path.join(t, "compare", "index.json"), "w"))
        roles = site_roles(t, manifest={"base_url": "http://client.test"})
        assert roles["compare/comp-b"] == "ours", roles
        # an explicit role beats everything
        json.dump({"sites": [{"slug": "ours-x", "role": "competitor"}]},
                  open(os.path.join(t, "compare", "index.json"), "w"))
        roles = site_roles(t, manifest={})
        assert roles["compare/ours-x"] == "competitor", roles
        assert is_ours("clarity", roles) and is_ours("compare", roles)
        assert not is_ours("compare/ours-x/clarity", roles)
    print("PASS")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(self_test())
