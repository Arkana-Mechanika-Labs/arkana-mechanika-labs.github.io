#!/usr/bin/env python3
"""Generate the public original-bugs catalogue from darklands-engine sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE_FILES = {
    "known": Path("docs/KNOWN_ORIGINAL_BUGS.md"),
    "dormant": Path("docs/DORMANT_ORIGINAL_BRANCHES.md"),
    "reported": Path("docs/research/DARKLANDS_483_07_REPORTED_BUG_CATALOGUE.md"),
}

REPORTED_SECTIONS = {
    "Historical defects not applicable to faithful 483.07 behavior": "Historical defects fixed before 483.07",
    "Officially reported surviving 483.07 issues": "Officially reported surviving 483.07 issues",
    "Inventory and numeric boundary reports": "Inventory and numeric boundaries",
    "Deterministic data and gameplay reports": "Data and gameplay reports",
    "Potion behavior and description mismatches": "Potion and description mismatches",
    "Tentative runtime and content reports": "Tentative runtime and content reports",
    "Forensic save signatures": "Forensic save signatures",
    "Documentation and deliberate limitations": "Documentation, platform issues, and deliberate mechanics",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group(1).strip(), text[match.end() : end].strip()))
    return result


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def first_table(body: str) -> tuple[list[str], list[list[str]], int]:
    lines = body.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().startswith("|")), -1)
    if start < 0 or start + 1 >= len(lines):
        return [], [], 0
    table_lines: list[str] = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            break
        table_lines.append(line)
    if len(table_lines) < 2:
        return [], [], 0
    headers = split_table_row(table_lines[0])
    rows = [split_table_row(line) for line in table_lines[2:]]
    return headers, rows, start + len(table_lines)


def kv_table(body: str) -> tuple[dict[str, str], int]:
    headers, rows, table_end = first_table(body)
    if headers[:2] != ["Field", "Value"]:
        return {}, table_end
    return {row[0]: row[1] for row in rows if len(row) >= 2}, table_end


def prose_summary(body: str, start_line: int, paragraphs: int = 2) -> str:
    tail = "\n".join(body.splitlines()[start_line:])
    tail = re.split(r"\n(?:Supporting reconstruction report|Supporting audit|Evidence:|Runtime observation:)", tail, maxsplit=1)[0]
    blocks = [re.sub(r"\s+", " ", block.strip()) for block in re.split(r"\n\s*\n", tail) if block.strip()]
    blocks = [block for block in blocks if not block.startswith("```")]
    return "\n\n".join(blocks[:paragraphs])


def code_label(value: str) -> str:
    """Remove Markdown code fencing from values rendered as UI labels."""
    return value.replace("`", "").strip()


def parse_known(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for heading, body in sections(text):
        match = re.match(r"(DL-[A-Z-]+-\d+):\s*(.+)", heading)
        if not match:
            continue
        fields, table_end = kv_table(body)
        entries.append(
            {
                "id": match.group(1),
                "title": match.group(2),
                "status": fields.get("Status", ""),
                "affected": fields.get("Affected input")
                or fields.get("Affected action")
                or fields.get("Affected route")
                or fields.get("Affected presentation")
                or "",
                "disposition": fields.get("SDL disposition", ""),
                "original_units": fields.get("Original units") or fields.get("Original unit") or "",
                "summary": prose_summary(body, table_end),
            }
        )
    return entries


def parse_dormant(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for heading, body in sections(text):
        if heading == "Explicit non-dormant counterexamples":
            continue
        fields, table_end = kv_table(body)
        if not fields.get("Classification"):
            continue
        entries.append(
            {
                "title": heading,
                "classification": code_label(fields.get("Classification", "")),
                "text": fields.get("Text") or fields.get("Encoded text") or "",
                "owner": fields.get("Ordinary owner", ""),
                "effect": fields.get("Latent effect", ""),
                "disposition": fields.get("Faithful disposition", ""),
                "boundary": fields.get("First unresolved boundary", ""),
                "summary": prose_summary(body, table_end, paragraphs=1),
            }
        )
    return entries


def parse_reported(text: str) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    for heading, body in sections(text):
        public_title = REPORTED_SECTIONS.get(heading)
        if not public_title:
            continue
        headers, rows, _ = first_table(body)
        if not headers:
            continue
        entries: list[dict[str, str]] = []
        for row in rows:
            values = dict(zip(headers, row))
            status = code_label(values.get("Status", ""))
            if status == "byte_confirmed":
                # The canonical known-bug tier already renders these entries.
                continue
            entries.append(
                {
                    "id": code_label(values.get("ID", "")),
                    "report": values.get("Report") or values.get("Forensic observation") or "",
                    "status": status,
                    "confidence": values.get("Confidence", ""),
                    "note": values.get("Suggested evidence target")
                    or values.get("Suggested boundary tests")
                    or values.get("Research note")
                    or values.get("Note")
                    or "",
                }
            )
        groups.append({"title": public_title, "source_heading": heading, "entries": entries})
    return groups


def generate(engine_root: Path) -> dict[str, object]:
    resolved = {name: engine_root / path for name, path in SOURCE_FILES.items()}
    missing = [str(path) for path in resolved.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing canonical source files: " + ", ".join(missing))

    commit = subprocess.run(
        ["git", "-C", str(engine_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    commit_date = subprocess.run(
        ["git", "-C", str(engine_root), "show", "-s", "--format=%cs", commit],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    known = parse_known(resolved["known"].read_text(encoding="utf-8"))
    dormant = parse_dormant(resolved["dormant"].read_text(encoding="utf-8"))
    reported = parse_reported(resolved["reported"].read_text(encoding="utf-8"))
    if not known or not dormant or not reported:
        raise RuntimeError("A canonical catalogue parsed as empty; refusing to publish partial data")

    return {
        "schema": "darklands.original-oddities.public.v1",
        "source_commit": commit,
        "source_commit_date": commit_date,
        "source_files": [
            {"path": SOURCE_FILES[name].as_posix(), "sha256": sha256(path)}
            for name, path in resolved.items()
        ],
        "counts": {
            "byte_confirmed": len(known),
            "dormant_groups": len(dormant),
            "reported_leads": sum(len(group["entries"]) for group in reported),
        },
        "known": known,
        "dormant": dormant,
        "reported_groups": reported,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine-root", type=Path, default=Path(__file__).resolve().parents[2] / "darklands-engine")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "original_oddities.json")
    parser.add_argument("--check", action="store_true", help="Fail when the generated data differs from the checked-in snapshot")
    args = parser.parse_args()

    payload = generate(args.engine_root.resolve())
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        current = args.output.read_text(encoding="utf-8") if args.output.is_file() else ""
        if current != rendered:
            print("Original bugs and oddities data is stale. Run the sync tool without --check.")
            return 1
        print(f"Original bugs and oddities data is current ({payload['source_commit'][:8]}).")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    counts = payload["counts"]
    print(
        f"Wrote {args.output}: {counts['byte_confirmed']} byte-confirmed, "
        f"{counts['dormant_groups']} dormant groups, {counts['reported_leads']} reported leads."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
