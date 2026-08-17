from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


MAX_CHARS = 3800
DIRECTIVE = "[Sound] no music"

MUSIC_PATTERNS = tuple(
    re.compile(pattern, flags=re.IGNORECASE | re.DOTALL)
    for pattern in (
        r"\b(?:bgm|ost|soundtrack)\b",
        r"\bbackground\s+music\b",
        r"\b(?:cinematic|dramatic|background|orchestral|instrumental|musical)\s+score\b",
        r"\b(?:instrumental|orchestral|rhythmic|rhythm-driven)\s+(?:track|accompaniment)\b",
        r"\bmelodic\s+whistl(?:e|es|ing)\b",
        r"\b(?:rising|falling|soft|loud|haunting|gentle|dramatic)\s+melod(?:y|ies)\b",
        r"\b(?:a|the)\s+song\s+(?:begins?|starts?|plays?|swells?|continues?|is\s+heard)\b",
        r"\b(?:she|he|they|the\s+(?:singer|vocalist|character|woman|man|child))\s+(?:is\s+|begins?\s+to\s+)?(?:sing(?:s|ing)?|hum(?:s|ming)?)\b",
        r"\b(?:band|orchestra|choir)\s+(?:performs?|plays?|starts?|begins?)\b",
        r"\b(?:singer|vocalist|guitarist|pianist|drummer|musician)\s+(?:performs?|plays?|sings?|strums?|drums?)\b",
        r"\b(?:audience|crowd|dancers?)\b.{0,80}\b(?:moves?|jumps?|sways?|dances?)\s+(?:in\s+time\s+with|to)\s+(?:the\s+)?(?:beat|tempo|rhythm)\b",
        r"\b(?:beat[- ]sync(?:ed|ing)?|sync(?:ed|s|ing)?\s+to\s+the\s+beat)\b",
        r"\b(?:music|musical)\s+(?:begins?|starts?|plays?|swells?|builds?|fades?|continues?|track|performance|accompaniment)\b",
        r"배경\s*음악",
        r"음악(?:이|을|은|의)?\s*(?:시작|재생|흐르|들리|커지|고조|깔리)",
        r"노래(?:를|가)?\s*(?:부르|시작|들리|나오)",
        r"(?:가수|보컬).{0,20}노래",
        r"(?:밴드|악기|오케스트라).{0,20}연주",
        r"(?:관객|사람들).{0,30}(?:박자|비트|템포)에?\s*맞춰",
    )
)


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    unicode_chars: int
    utf16_units: int
    violations: tuple[str, ...]


def utf16_length(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


def music_language_present(prompt: str) -> bool:
    masked = prompt.replace(DIRECTIVE, "")
    return any(pattern.search(masked) for pattern in MUSIC_PATTERNS)


def validate_prompt(prompt: str) -> ValidationResult:
    violations: list[str] = []
    unicode_chars = len(prompt)
    utf16_units = utf16_length(prompt)
    if not prompt:
        violations.append("empty")
    if unicode_chars > MAX_CHARS:
        violations.append("unicode-length")
    if utf16_units > MAX_CHARS:
        violations.append("utf16-length")
    if prompt.count(DIRECTIVE) != 1:
        violations.append("sound-directive-count")
    if music_language_present(prompt):
        violations.append("music-language")
    if "```" in prompt:
        violations.append("code-fence")
    return ValidationResult(
        ok=not violations,
        unicode_chars=unicode_chars,
        utf16_units=utf16_units,
        violations=tuple(violations),
    )


def read_prompt(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    args = parser.parse_args(argv)
    try:
        prompt = read_prompt(args.path)
    except (OSError, UnicodeError) as error:
        print(f"error: cannot read prompt: {error}", file=sys.stderr)
        return 2
    result = validate_prompt(prompt)
    print(
        f"ok={str(result.ok).lower()} "
        f"unicode_chars={result.unicode_chars} "
        f"utf16_units={result.utf16_units} "
        f"violations={','.join(result.violations) or 'none'}"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
