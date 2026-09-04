"""Build portable downloads from one canonical skill (Python standard library)."""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "video-prompt-maker"
FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/validate_prompt.py",
    "references/acting-performance.md",
    "references/prompt-architecture.md",
    "references/quality-check.md",
    "references/spatial-physics.md",
    "references/visual-continuity.md",
)
WEB_HEADER = """# Video Prompt Maker — Web Instructions

Created by Contentrium. This is an instructions-only adaptation, not a native
skill installation. Automatic skill discovery and script execution depend on the
host and are not provided by attaching this file.

## Setup

Attach this complete file as knowledge to a Gem, Project, or comparable assistant.
Paste the following short instruction into that assistant's instruction field:

> For video-generation prompt requests, use Video Prompt Maker from the attached
> complete Web Instructions file. Read its SKILL.md section and the references
> routed there before drafting. Apply every output rule and exclusion. Treat the
> labelled file sections as the skill's virtual files. If a required section is
> inaccessible, ask for it. If execution is available, run the bundled Python
> validator on the exact prompt body. Otherwise mark the output as an unverified
> draft and state that deterministic validation remains required; never claim a
> check ran when it did not. Do not generate a video or install software.

Keep the full attachment: do not truncate its policy or reference sections to fit
an instruction field. A chat without persistent instructions can use the same
instruction and complete attachment for that chat only. If the host cannot read
this file or has insufficient context capacity, use a native skill-capable host.

## Bundled files

The following sections are copied in full from the canonical skill. File paths
name sections here; they are not promises that a web host has a local filesystem.
The Python source is a validation tool, not prose to paste into a video prompt.

"""


def build(output_dir: Path, timestamp: str) -> list[Path]:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}'\d{2}", timestamp):
        raise ValueError("timestamp must have the form YYYY-MM-DD HH'mm")
    datetime.strptime(timestamp, "%Y-%m-%d %H'%M")
    payload = {}
    for name in FILES:
        source = SKILL / name
        if source.is_symlink() or not source.resolve().is_relative_to(SKILL.resolve()):
            raise ValueError(f"source must stay inside the skill directory: {name}")
        payload[name] = source.read_bytes()

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in payload.items():
            info = zipfile.ZipInfo(f"video-prompt-maker/{name}", (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)

    # Native metadata belongs in the archive; the web version needs instructions
    # and validator source, not host-specific UI configuration.
    sections = [WEB_HEADER]
    for name in ("SKILL.md", *(n for n in FILES if n.startswith("references/")),
                 "scripts/validate_prompt.py"):
        body = payload[name].decode("utf-8").replace("\r\n", "\n").strip()
        sections.append(f"\n---\n\n## File: {name}\n\n")
        if name.endswith(".py"):
            sections.append(f"````python\n{body}\n````\n")
        else:
            sections.append(body + "\n")

    downloads = {
        f"{timestamp} Video Prompt Maker.zip": buffer.getvalue(),
        f"{timestamp} Video Prompt Maker.skill": buffer.getvalue(),
        f"{timestamp} Video Prompt Maker Web Instructions.md": "".join(sections).encode("utf-8"),
    }
    checksums = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n"
                        for name, data in downloads.items())
    downloads["SHA256SUMS.txt"] = checksums.encode("utf-8")
    for name in downloads:
        if (output_dir / name).exists():
            raise FileExistsError(f"refusing to overwrite existing release: {name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in downloads.items():
        with (output_dir / name).open("xb") as handle:
            handle.write(data)
    return [output_dir / name for name in downloads]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--timestamp", default=datetime.now().astimezone().strftime("%Y-%m-%d %H'%M"),
                        help="Download filename prefix, default: local completion time")
    args = parser.parse_args()
    try:
        paths = build(args.output_dir, args.timestamp)
    except (OSError, ValueError) as error:
        parser.exit(1, f"error: {error}\n")
    for path in paths:
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
