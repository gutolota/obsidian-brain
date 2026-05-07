#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════
#  Obsidian Brain — Skill Setup
#
#  Installs the obsidian-brain skill family into ~/.claude/skills/
#  Each skill provides a slash command:
#    /obsidian-brain                — dynamic dispatcher
#    /obsidian-brain:process        — full + offer compact
#    /obsidian-brain:quick-sync     — lightweight checkpoint
#    /obsidian-brain:learn          — teach a rule
#    /obsidian-brain:status         — show config and rules
#
#  User data (config.md, brain-rules.md) lives in
#  ~/.claude/obsidian-brain/ — preserved across reinstalls.
# ══════════════════════════════════════════════════════════
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
DIM='\033[2m'
NC='\033[0m'

CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
DATA_DIR="$CLAUDE_DIR/obsidian-brain"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${CYAN}┌──────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│   🧠 Obsidian Brain — Skill Setup         │${NC}"
echo -e "${CYAN}└──────────────────────────────────────────┘${NC}"
echo ""

# ── 1. Create directories ───────────────────────────────
mkdir -p "$SKILLS_DIR" "$DATA_DIR"

# ── 2. Install skills ────────────────────────────────────
echo -e "${DIM}Installing skills...${NC}"

# Each skill is a directory with a SKILL.md inside.
# The folder name on disk doesn't matter — the `name:` in frontmatter
# is what becomes the slash command (with `:` for namespacing).

for skill_src_dir in "$SCRIPT_DIR/skills/"*/; do
    skill_name=$(basename "$skill_src_dir")
    target="$SKILLS_DIR/$skill_name"

    # Always overwrite the skill itself — it's the prompt logic
    rm -rf "$target"
    cp -r "$skill_src_dir" "$target"

    # Read the slash command name from frontmatter for display
    slash_cmd=$(grep -m1 '^name:' "$target/SKILL.md" | sed 's/name: *//')
    echo -e "  ${GREEN}✓${NC} /${slash_cmd}"
done

# ── 3. Bootstrap user data (preserve if exists) ──────────
echo ""
echo -e "${DIM}Setting up user data...${NC}"

if [ ! -f "$DATA_DIR/config.md" ]; then
    cp "$SCRIPT_DIR/data/config.md" "$DATA_DIR/config.md"
    echo -e "  ${GREEN}✓${NC} config.md ${DIM}(new — edit your vault path!)${NC}"
else
    echo -e "  ${YELLOW}→${NC} config.md already exists ${DIM}(preserved)${NC}"
fi

if [ ! -f "$DATA_DIR/brain-rules.md" ]; then
    cp "$SCRIPT_DIR/data/brain-rules.md" "$DATA_DIR/brain-rules.md"
    echo -e "  ${GREEN}✓${NC} brain-rules.md ${DIM}(new)${NC}"
else
    echo -e "  ${YELLOW}→${NC} brain-rules.md already exists ${DIM}(preserved — has learned rules)${NC}"
fi

# ── 4. Install kepano's obsidian-skills (companion) ──────
echo ""
echo -e "${DIM}Installing kepano's obsidian-skills (formatting helpers)...${NC}"

if command -v git &>/dev/null; then
    TEMP=$(mktemp -d)
    if git clone --depth=1 --quiet https://github.com/kepano/obsidian-skills.git "$TEMP" 2>/dev/null; then
        for skill_dir in "$TEMP/skills/"*/; do
            kep_name=$(basename "$skill_dir")
            if [ -d "$skill_dir" ] && [ ! -d "$SKILLS_DIR/$kep_name" ]; then
                cp -r "$skill_dir" "$SKILLS_DIR/$kep_name"
                echo -e "  ${GREEN}✓${NC} $kep_name"
            elif [ -d "$SKILLS_DIR/$kep_name" ]; then
                echo -e "  ${YELLOW}→${NC} $kep_name ${DIM}(already installed)${NC}"
            fi
        done
        rm -rf "$TEMP"
    else
        echo -e "  ${YELLOW}⚠${NC} Clone failed — install manually if desired:"
        echo -e "    ${DIM}git clone https://github.com/kepano/obsidian-skills.git${NC}"
        echo -e "    ${DIM}cp -r obsidian-skills/skills/* ~/.claude/skills/${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} git not found — skip kepano's skills"
fi

# ── 5. Summary ────────────────────────────────────────────
echo ""
echo -e "${GREEN}┌──────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│   ✅  Installation complete!              │${NC}"
echo -e "${GREEN}└──────────────────────────────────────────┘${NC}"
echo ""
echo "  Available slash commands (in any Claude Code session):"
echo ""
echo -e "    ${CYAN}/obsidian-brain${NC}              ${DIM}— dynamic dispatcher${NC}"
echo -e "    ${CYAN}/obsidian-brain:process${NC}      ${DIM}— full + offer /compact${NC}"
echo -e "    ${CYAN}/obsidian-brain:quick-sync${NC}   ${DIM}— lightweight checkpoint${NC}"
echo -e "    ${CYAN}/obsidian-brain:learn${NC}        ${DIM}— teach a permanent rule${NC}"
echo -e "    ${CYAN}/obsidian-brain:status${NC}       ${DIM}— show config and rules${NC}"
echo ""
echo "  Next steps:"
echo ""
echo -e "  1. ${CYAN}Edit your vault path:${NC}"
echo -e "     ${DIM}$DATA_DIR/config.md${NC}"
echo ""
echo -e "  2. ${CYAN}Try it:${NC} in any project, run ${CYAN}/obsidian-brain:status${NC}"
echo ""
echo -e "  ${DIM}Re-run setup.sh anytime — config and learned rules are preserved.${NC}"
echo ""
