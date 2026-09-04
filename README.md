# Video Prompt Maker

**An Agent Skill by Contentrium.**

콘텐츠리움이 제작한 영상 생성 프롬프트용 Agent Skill입니다. 특정 에이전트나 앱에만 종속되지 않으며, Agent Skills를 지원하는 도구에서 같은 핵심 지침을 사용할 수 있습니다.

Video Prompt Maker turns video-prompt requests into structured prompts for Seedance, Veo, Kling, Sora, Runway, and other video models.

## Core behavior

- Writes prompt bodies in English while preserving exact Korean dialogue and on-screen text.
- Uses the order: Subject + Motion → Environment → Camera → Style → Sound → Constraints.
- Supports text-to-video, image-to-video, reference-to-video, multi-shot, and storyboard-to-video requests.
- Uses one camera movement per shot and observable acting direction.
- Delivers each finished prompt in its own copy-ready code block.

## Package layout

The canonical skill folder is `skills/video-prompt-maker`. Keep that folder intact when installing: the installed folder must contain `SKILL.md` directly, not an additional nested `video-prompt-maker` folder.

```text
skills/video-prompt-maker/
├── SKILL.md
├── agents/
│   └── openai.yaml              # Optional Codex UI metadata; not required at runtime
├── scripts/
│   └── validate_prompt.py
└── references/
    ├── acting-performance.md
    ├── prompt-architecture.md
    ├── quality-check.md
    ├── spatial-physics.md
    └── visual-continuity.md
```

`SKILL.md`, its references, and the validator are the portable skill content. `agents/openai.yaml` is optional metadata for the Codex UI only; it is not needed for other tools or for runtime behavior.

## Install manually

Copy the canonical `video-prompt-maker` folder into the relevant skills directory, so the destination ends in `video-prompt-maker/SKILL.md`.

| Tool | Project-level skills directory | User-level skills directory |
| --- | --- | --- |
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| Gemini CLI | `.gemini/skills` | `~/.gemini/skills` |
| Codex | `.agents/skills` | `~/.agents/skills` (legacy `.codex/skills` also works) |
| GitHub Copilot | `.github/skills` | `~/.copilot/skills` |
| Windsurf | `.windsurf/skills` | `~/.codeium/windsurf/skills` |

For example, a project installation creates `.claude/skills/video-prompt-maker/SKILL.md`; a user installation creates `~/.claude/skills/video-prompt-maker/SKILL.md`. On Windows, `~` means your user-profile folder (for example, `C:\Users\your-name`). Reload or restart the relevant tool after installation; skill discovery and enabling may also depend on that tool's settings.

## Gemini CLI

Gemini CLI can install this skill directly from the repository:

```bash
gemini skills install https://github.com/contentriumkorea/video-prompt-maker.git --path skills/video-prompt-maker --scope user
gemini skills list
```

For a local archive install, Gemini CLI expects a `.skill` archive, not an ordinary `.zip` file.

## Optional community installer

If Node.js and npm are already available, the Vercel community installer can optionally install this skill:

```bash
npx skills add contentriumkorea/video-prompt-maker --skill video-prompt-maker
```

It interactively lets you choose clients. Review those choices yourself; this README does not recommend installing to every client or bypassing consent prompts. This is a third-party community tool, not a required dependency. No custom installer, plugin, or extension is required.

## Use the release package in web tools

The [latest release](https://github.com/contentriumkorea/video-prompt-maker/releases/latest) includes a release ZIP, a `.skill` archive, and a **Web Instructions** Markdown file. Download names include a timestamp; GitHub may replace spaces and punctuation with dots.

For Gemini web/Gems and other tools without native Agent Skill installation, use that instruction file:

1. Paste its compact front section into the tool's custom instructions.
2. Attach the same complete file as knowledge/context so the full canonical skill, references, and validator source remain available.

Do not truncate the instructions to fit a UI limit; attach the complete file when necessary. This text-based fallback cannot provide automatic skill triggers or guarantee executable validation. Use manual or code-enabled validation where available, and do not claim that validation passed unless it was actually executed.

Claude web can upload a ZIP containing one top-level `video-prompt-maker/SKILL.md` folder through **Customize > Skills**, when the feature is available and enabled for the account. See [Claude skills uploads](https://claude.com/docs/skills/how-to).

## Validate a prompt

The validator requires Python 3.10 or later and only uses the Python standard library.

From the skill root:

```powershell
python scripts/validate_prompt.py prompt.txt
```

From outside the skill root, use an absolute path to the validator and to the prompt file:

```powershell
python "C:\path\to\video-prompt-maker\scripts\validate_prompt.py" "C:\path\to\prompt.txt"
```

Exit codes:

- `0`: valid prompt
- `1`: prompt-policy violation
- `2`: file or decoding error

The validator checks the skill's core output contract and code-fence leakage. A successful result only represents checks that were run; it does not test a particular app or model.

## Maintainers

Build release artifacts:

```powershell
python tools/build_release.py --output-dir dist
```

The builder keeps local download names intact. When publishing on GitHub, use the final uploaded asset names in the published `SHA256SUMS.txt`; GitHub normalizes spaces and punctuation. Keep the hashes unchanged and verify the uploaded bytes before publishing the release.

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor skills](https://cursor.com/docs/skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [VS Code agent skills / GitHub Copilot](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Windsurf Cascade skills](https://docs.windsurf.com/windsurf/cascade/skills)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Gemini Gems](https://support.google.com/gemini/answer/15235603?hl=en)
- [Vercel community skills installer](https://github.com/vercel-labs/skills)

## Credits

Created and maintained by **Contentrium**.
