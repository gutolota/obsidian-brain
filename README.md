# 🧠 Obsidian Brain — Claude Code Skill Family

A family of agent skills for Claude Code that processes your sessions and syncs them to your Obsidian vault — with dynamic dispatch, namespaced commands, and a learning system that grows over time.

---

## What you get

Five slash commands, all available globally in any Claude Code session:

| Command | What it does |
|---------|--------------|
| `/obsidian-brain` | **Dynamic dispatcher** — reads your intent from arguments and delegates |
| `/obsidian-brain:process` | **End-of-session** — deep extraction + offer `/compact` |
| `/obsidian-brain:quick-sync` | **Mid-session** — lightweight checkpoint, no compact |
| `/obsidian-brain:learn` | **Teach a rule** — adds to `brain-rules.md` permanently |
| `/obsidian-brain:status` | **Inspect** — show config, learned rules, monitored projects |

All implemented as **agent skills** (Claude Code v2.1.101+). They live in `~/.claude/skills/` and are invoked either directly or auto-discovered by Claude based on your phrasing.

---

## Why a skill family (not one skill)

Claude Code's skill system uses descriptions to decide which skill to load. Splitting into specialized skills means:

1. **Direct invocation** — `/obsidian-brain:process` skips dispatcher overhead and goes straight to the right behavior
2. **Better auto-discovery** — when you say "save this and compact", Claude matches `obsidian-brain:process` directly without ambiguity
3. **Cleaner separation** — each skill has a tight focus and only loads the references it needs

The main `/obsidian-brain` skill remains as a smart dispatcher for when you want flexibility (e.g., free-text input, ambiguous intent).

---

## Architecture

```
~/.claude/
├── skills/
│   ├── obsidian-brain/                 ← dispatcher + shared references
│   │   ├── SKILL.md                    name: obsidian-brain
│   │   └── references/
│   │       ├── extraction.md           ← what to pull from a conversation
│   │       ├── daily-note.md           ← format + smart-append logic
│   │       ├── learning.md             ← detecting meta-instructions
│   │       ├── obsidian-formatting.md  ← wikilinks, callouts, properties
│   │       └── defaults.md             ← bootstrap content
│   ├── obsidian-brain-process/
│   │   └── SKILL.md                    name: obsidian-brain:process
│   ├── obsidian-brain-quick-sync/
│   │   └── SKILL.md                    name: obsidian-brain:quick-sync
│   ├── obsidian-brain-learn/
│   │   └── SKILL.md                    name: obsidian-brain:learn
│   ├── obsidian-brain-status/
│   │   └── SKILL.md                    name: obsidian-brain:status
│   └── obsidian-*/                     ← kepano's obsidian-skills
│
└── obsidian-brain/                     ← USER DATA for Claude Code
    ├── config.md                       ← vault path, folders, behavior
    └── brain-rules.md                  ← LIVING document — grows over time

~/.gemini/obsidian-brain/               ← USER DATA for Gemini CLI / Antigravity
~/.codex/obsidian-brain/                ← USER DATA for Codex CLI
```

Skill source files use `{BRAIN_DATA_DIR}` as a path token. Each setup/install script substitutes it with the agent-specific path at install time — so installed skills always reference the correct directory for that agent.

The folder name on disk is just a folder name. The `name:` field in each `SKILL.md` frontmatter is what becomes the slash command — that's where the `:` namespacing lives.

User data sits **outside** the skills directory so reinstalls never wipe your learned rules.

## Progressive disclosure

The dispatcher skill (`obsidian-brain/SKILL.md`) is concise — it routes intent and points to references for details. The references load only when needed:

- Doing extraction? → load `references/extraction.md`
- Updating a daily note? → load `references/daily-note.md`
- Detecting a new rule? → load `references/learning.md`

This keeps the prompt context small for trivial calls (like `status`) while still providing depth for complex ones (like `process`).

---

## Installation

### By agent

| Agent | Platform | Install |
|-------|----------|---------|
| **Claude Code** | Linux / macOS | `./setup.sh` or `npx skills add` (see below) |
| **Claude Code** | Windows | `.\setup.ps1` in PowerShell |
| **Gemini CLI / Antigravity** | Linux / macOS | `./adapters/gemini/install.sh` |
| **OpenAI Codex CLI** | Linux / macOS | `./adapters/codex/install.sh` |

Each agent gets its own data directory — brain rules are agent-specific by default.

### Data directory by agent and OS

| Agent | Linux / macOS | Windows |
|-------|--------------|---------|
| Claude Code | `~/.claude/obsidian-brain/` | `%APPDATA%\Claude\obsidian-brain\` |
| Gemini CLI | `~/.gemini/obsidian-brain/` | _(use WSL)_ |
| Codex CLI | `~/.codex/obsidian-brain/` | _(use WSL)_ |

---

### Claude Code — Option 1: npx (no clone needed)

```bash
npx skills add https://github.com/gutolota/obsidian-brain
```

Installs all skills directly to `~/.claude/skills/`. Then run `/obsidian-brain:status` once in any Claude Code session — this bootstraps your config and rules files on first use.

Finally, point the brain at your vault:

```bash
nano ~/.claude/obsidian-brain/config.md   # set Vault path and Daily Notes folder
```

> **Want the short form?** Once the repo is listed on [skills.sh](https://skills.sh), you'll be able to use `npx skills add gutolota/obsidian-brain`.

---

### Claude Code — Option 2: setup script (includes kepano's obsidian-skills)

```bash
git clone https://github.com/gutolota/obsidian-brain
cd obsidian-brain
chmod +x setup.sh
./setup.sh              # Linux / macOS
# .\setup.ps1           # Windows (PowerShell)
```

The setup script does everything npx does, plus:
- Substitutes the correct data directory path into installed skill files
- Installs [kepano's obsidian-skills](https://github.com/kepano/obsidian-skills) as companion formatting helpers (Obsidian Markdown, CLI, Bases, Canvas)
- Pre-creates `config.md` and `brain-rules.md` with sane defaults — no need to trigger bootstrap manually

Re-running is safe — your config and learned rules are never overwritten.

After install, edit `~/.claude/obsidian-brain/config.md` with your real vault path.

---

### Gemini CLI / Antigravity

```bash
git clone https://github.com/gutolota/obsidian-brain
cd obsidian-brain
./adapters/gemini/install.sh
```

Then edit `~/.gemini/obsidian-brain/config.md` with your vault path.

In any Gemini session, use natural language: `"sync to obsidian"`, `"save session"`, `"wrap up"`.

See [`adapters/gemini/README.md`](adapters/gemini/README.md) for details.

---

### OpenAI Codex CLI

```bash
git clone https://github.com/gutolota/obsidian-brain
cd obsidian-brain
./adapters/codex/install.sh
```

Then edit `~/.codex/obsidian-brain/config.md` with your vault path.

See [`adapters/codex/README.md`](adapters/codex/README.md) for details.

---

### After install (Claude Code)

| File | Purpose | Edit? |
|------|---------|-------|
| `~/.claude/obsidian-brain/config.md` | Vault path, folders, write mode | ✅ Yes — set your vault path |
| `~/.claude/obsidian-brain/brain-rules.md` | Learned rules (grows over time) | Optional — or let the brain manage it |
| `~/.claude/skills/obsidian-brain*/` | Skill logic | ❌ No — updated by reinstalling |

---

## Usage examples

### End-of-session wrap-up

```
/obsidian-brain:process
```

Deep extraction → daily note updated → all learned rules executed → asks: _"Run /compact?"_

### Mid-session checkpoint

```
/obsidian-brain:quick-sync
```

Quick append to today's daily note, no interruption to flow.

### Teach a permanent rule

```
/obsidian-brain:learn always log every npm package I install in Tooling/installs.md
```

Saved to `brain-rules.md`. Applied to every future sync across all projects.

### Dynamic dispatch (free text)

```
/obsidian-brain focus on the database migration decisions and save it
```

The dispatcher reads "save it" → routes to quick-sync, with the focus area applied.

### Inspect state

```
/obsidian-brain:status
```

Shows vault path, learned rule count, monitored projects.

---

## Learning over time

The brain detects **meta-instructions** in your conversations. If you say:

> "I want you to keep a separate file with tech debt items"

…the next time `process` or `quick-sync` runs, it adds this rule to `brain-rules.md` under `## Learned Rules` with the date. From then on, every sync will check for tech debt items and maintain that file.

You can also teach explicitly:
```
/obsidian-brain:learn maintain Projects/<project>/tech-debt.md with items tagged #tech-debt
```

Either way, rules accumulate. The brain never forgets unless you edit `brain-rules.md` manually.

---

## Daily note example

After a few `process` runs throughout the day:

```markdown
---
date: 2026-05-06
tags: [daily-note]
aliases: [Tuesday]
---

# 2026-05-06 — Tuesday

## Sessions

### 10:30 — my-api · JWT auth middleware
Implemented token validation middleware for v2 routes. Decided on
RS256 over HS256 for asymmetric verification.

> [!summary] Decisions
> - RS256 over HS256 — keys can be rotated independently
> - Middleware before rate limiting, not after

**Files:** `src/middleware/auth.ts`, `src/types/jwt.ts`

### 14:15 — my-api · Database migration for roles
Added roles table and user-role junction. Seeded admin and viewer.

> [!summary] Decisions
> - Separate roles table over enum — extensible without migrations
> - Soft delete on assignments, hard delete on roles

**Files:** `migrations/003_roles.sql`, `src/models/role.ts`

## Tasks

- [ ] Write integration tests for auth middleware
- [ ] Add rate limiting per role tier
- [ ] Document permission model in README

## Notes

- pg_trgm extension needed for fuzzy role name search
```

---

## Tips

- **Use `:process` at end of day or before switching tasks** — the compact offer keeps your context fresh
- **Use `:quick-sync` mid-flow** — it's brief and doesn't break concentration
- **Teach rules early** — the more you teach, the more useful the brain becomes
- **Edit `brain-rules.md` manually anytime** — it's just markdown
- **Skills auto-discover** — even without typing the exact command, Claude can find the right skill if you describe the intent
