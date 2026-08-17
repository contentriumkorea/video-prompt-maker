# Video Prompt Maker

**A Codex skill by Contentrium.**

콘텐츠리움이 제작한 영상 생성 프롬프트용 Codex 스킬입니다.

Video Prompt Maker converts video-prompt requests into a consistent Seedance 2.0 house style, even when the request names another model such as Veo, Kling, Sora, Runway, or another video generator.

## Core behavior

- Writes prompt bodies in English while preserving exact Korean dialogue and on-screen text.
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

The validator checks the skill's core output contract and code-fence leakage.

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
