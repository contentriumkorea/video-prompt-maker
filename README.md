# Video Prompt Maker

**A Codex skill by Contentrium.**

콘텐츠리움이 제작한 영상 생성 프롬프트용 Codex 스킬입니다.

Video Prompt Maker converts video-prompt requests into a consistent Seedance 2.0 house style, even when the request names another model such as Veo, Kling, Sora, Runway, or another video generator.

## Core behavior

- Writes prompt bodies in English while preserving exact Korean dialogue and on-screen text.
- Enforces a hard maximum of 3,800 Unicode characters and 3,800 UTF-16 code units.
- Includes the exact directive `[Sound] no music` once in every video prompt.
- Removes music-generation instructions and asks for a non-musical replacement when music is indispensable to the requested concept.
- Uses the order: Subject + Motion → Environment → Camera → Style → Sound → Constraints.
- Supports text-to-video, image-to-video, reference-to-video, multi-shot, and storyboard-to-video requests.
- Uses one camera movement per shot and observable acting direction.
- Delivers each finished prompt in its own copy-ready code block.

## Install

Ask Codex:

> Install the `video-prompt-maker` skill from https://github.com/contentriumkorea/video-prompt-maker/tree/main/skills/video-prompt-maker

If the skill does not appear immediately, open a new Codex task or restart Codex so the skill catalog reloads.

For a manual installation, copy `skills/video-prompt-maker` into:

```text
$CODEX_HOME/skills/video-prompt-maker
```

## Validate a prompt

```powershell
python skills/video-prompt-maker/scripts/validate_prompt.py prompt.txt
```

Exit codes:

- `0`: valid prompt
- `1`: prompt-policy violation
- `2`: file or decoding error

The validator checks length, the exact sound directive, code-fence leakage, and high-confidence music-generation language.

## Important limitation

The 3,800-character limit and exact sound directive are Contentrium house rules, not official Seedance syntax. Prompt wording alone cannot guarantee that a stochastic video model will never generate music. For a hard audio guarantee, disable generated audio entirely when the platform supports it and add only approved dialogue or effects in post-production.

## Skill package

```text
skills/video-prompt-maker/
├── SKILL.md
├── agents/openai.yaml
├── scripts/validate_prompt.py
└── references/
    ├── acting-performance.md
    ├── prompt-architecture.md
    ├── quality-check.md
    ├── spatial-physics.md
    └── visual-continuity.md
```

## Credits

Created and maintained by **Contentrium**.
