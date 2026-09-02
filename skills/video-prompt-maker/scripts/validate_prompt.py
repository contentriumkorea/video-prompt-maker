from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MODEL = "Seedance 2.0"
MODEL_LIMITS = {
    "Seedance 2.0": 3800,
    "Seedance 2.5": 14000,
    "MiniMax H3": 6500,
    "Kling 3.0": 8000,
}
MODEL_SLUGS = {
    "Seedance 2.0": "seedance-2.0",
    "Seedance 2.5": "seedance-2.5",
    "MiniMax H3": "minimax-h3",
    "Kling 3.0": "kling-3.0",
}
MODEL_ALIASES = {
    "Seedance 2.0": ("Seedance 2.0", "시댄스 2.0"),
    "Seedance 2.5": ("Seedance 2.5", "시댄스 2.5"),
    "MiniMax H3": ("MiniMax H3", "미니맥스 H3"),
    "Kling 3.0": ("Kling 3.0", "Kling 3", "클링 3.0", "클링 3"),
}
# Backward-compatible alias for callers that imported the original default cap.
MAX_CHARS = MODEL_LIMITS[DEFAULT_MODEL]
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
class ModelPolicy:
    model: str
    max_chars: int
    slug: str


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    unicode_chars: int
    utf16_units: int
    violations: tuple[str, ...]
    model: str = DEFAULT_MODEL
    max_chars: int = MAX_CHARS


def normalize_model_name(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.casefold())


ALIAS_TO_MODEL = {
    normalize_model_name(alias): model
    for model, aliases in MODEL_ALIASES.items()
    for alias in aliases
}


def split_model_names(value: str) -> list[str]:
    return [
        part.strip()
        for part in re.split(
            r"\s*(?:,|/|\||\+|&|\band\b|및|와|과)\s*",
            value,
            flags=re.IGNORECASE,
        )
        if part.strip()
    ]


def resolve_model_policy(model: str | Iterable[str] | None = None) -> ModelPolicy:
    if model is None:
        requested: list[str] = []
    elif isinstance(model, str):
        requested = split_model_names(model)
    else:
        requested = [
            part
            for value in model
            for part in split_model_names(str(value))
        ]

    if not requested:
        requested = [DEFAULT_MODEL]

    resolved = [
        ALIAS_TO_MODEL.get(normalize_model_name(value), DEFAULT_MODEL)
        for value in requested
    ]
    selected = min(resolved, key=lambda name: MODEL_LIMITS[name])
    return ModelPolicy(
        model=selected,
        max_chars=MODEL_LIMITS[selected],
        slug=MODEL_SLUGS[selected],
    )


def utf16_length(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


def music_language_present(prompt: str) -> bool:
    masked = prompt.replace(DIRECTIVE, "")
    return any(pattern.search(masked) for pattern in MUSIC_PATTERNS)


def validate_prompt(
    prompt: str,
    model: str | Iterable[str] | None = None,
) -> ValidationResult:
    policy = resolve_model_policy(model)
    violations: list[str] = []
    unicode_chars = len(prompt)
    utf16_units = utf16_length(prompt)
    if not prompt:
        violations.append("empty")
    if unicode_chars > policy.max_chars:
        violations.append("unicode-length")
    if utf16_units > policy.max_chars:
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
        model=policy.model,
        max_chars=policy.max_chars,
    )


def read_prompt(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument(
        "--model",
        action="append",
        help=(
            "Target model. Repeat for a shared prompt; the smallest applicable "
            "limit is used. Defaults to Seedance 2.0."
        ),
    )
    args = parser.parse_args(argv)
    try:
        prompt = read_prompt(args.path)
    except (OSError, UnicodeError) as error:
        print(f"error: cannot read prompt: {error}", file=sys.stderr)
        return 2
    policy = resolve_model_policy(args.model)
    result = validate_prompt(prompt, model=args.model)
    print(
        f"ok={str(result.ok).lower()} "
        f"unicode_chars={result.unicode_chars} "
        f"utf16_units={result.utf16_units} "
        f"violations={','.join(result.violations) or 'none'} "
        f"model={policy.slug} "
        f"max_chars={result.max_chars}"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
