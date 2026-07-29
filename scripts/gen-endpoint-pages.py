#!/usr/bin/env python3
"""Generate the GitBook endpoint pages from api-reference/openapi.yaml.

GitBook renders each operation from an OpenAPI block that points at the spec
file in this repo. This script writes one page per OpenAPI tag, with one block
per operation, so the reference tracks the spec instead of being hand-kept.

Run it after scripts/sync-openapi.py, then add any new page to SUMMARY.md.

Usage:
    scripts/gen-endpoint-pages.py
"""

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SPEC = REPO / "api-reference" / "openapi.yaml"
OUT = REPO / "api-reference" / "endpoints"
# Path to the spec, relative to a page in OUT.
SRC = "../openapi.yaml"
METHODS = ("get", "post", "put", "patch", "delete")


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> None:
    spec = yaml.safe_load(SPEC.read_text())
    tags = spec.get("tags", [])

    by_tag: dict[str, list[tuple[str, str, dict]]] = {}
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method not in METHODS:
                continue
            for tag in op.get("tags", ["Other"]):
                by_tag.setdefault(tag, []).append((path, method, op))

    OUT.mkdir(parents=True, exist_ok=True)
    written = set()
    entries = []

    for tag in tags:
        name = tag["name"]
        ops = by_tag.get(name)
        if not ops:
            continue
        description = " ".join((tag.get("description") or "").split())
        front = yaml.safe_dump(
            {"description": description}, sort_keys=False, allow_unicode=True
        ).strip()

        lines = ["---", front, "---", "", f"# {name}", ""]
        for path, method, op in ops:
            heading = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
            lines += [
                f"## {heading}",
                "",
                f'{{% openapi src="{SRC}" path="{path}" method="{method}" %}}',
                f"[openapi.yaml]({SRC})",
                "{% endopenapi %}",
                "",
            ]

        page = OUT / f"{slug(name)}.md"
        page.write_text("\n".join(lines).rstrip() + "\n")
        written.add(page.name)
        entries.append((name, page.relative_to(REPO), len(ops)))
        print(f"wrote {page.relative_to(REPO)} ({len(ops)} operations)")

    stale = [p for p in OUT.glob("*.md") if p.name not in written]
    for p in stale:
        print(f"warning: {p.relative_to(REPO)} no longer matches a tag; delete it and its "
              "SUMMARY.md entry")

    print("\nSUMMARY.md entries for these pages:")
    for name, page, _ in entries:
        print(f"  * [{name}]({page})")


if __name__ == "__main__":
    main()
