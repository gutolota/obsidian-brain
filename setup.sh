#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════
#  Obsidian Brain — Setup
#
#  Installs the obsidian-brain skill family for one or more
#  coding agents. Re-running is always safe — user data
#  (config.md, brain-rules.md) is never overwritten.
# ══════════════════════════════════════════════════════════
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Agent definitions ────────────────────────────────────
# Format: "label|skill_src|skills_dst|data_dir|detect_cmd"
AGENTS=(
  "Claude Code|.claude/skills|$HOME/.claude/skills|$HOME/.claude/obsidian-brain|claude"
  "Gemini CLI / Antigravity|.gemini/skills|$HOME/.gemini/skills|$HOME/.gemini/obsidian-brain|gemini"
  "Universal — Codex, Cursor, Copilot +13 more|.agents/skills|$HOME/.agents/skills|$HOME/.agents/obsidian-brain|"
)

# ── Banner ───────────────────────────────────────────────
echo ""
echo -e "${CYAN}┌──────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│        🧠 Obsidian Brain — Setup          │${NC}"
echo -e "${CYAN}└──────────────────────────────────────────┘${NC}"
echo ""

# ── Detect installed agents ──────────────────────────────
detected=()
for entry in "${AGENTS[@]}"; do
  IFS='|' read -r label _ _ _ detect_cmd <<< "$entry"
  if [ -n "$detect_cmd" ] && command -v "$detect_cmd" &>/dev/null; then
    detected+=("$label")
  fi
done

if [ ${#detected[@]} -gt 0 ]; then
  echo -e "  ${DIM}Detected agents: ${detected[*]}${NC}"
  echo ""
fi

# ── Agent selection ──────────────────────────────────────
echo -e "  ${BOLD}Which agents do you want to install for?${NC}"
echo ""
i=1
for entry in "${AGENTS[@]}"; do
  IFS='|' read -r label _ _ _ detect_cmd <<< "$entry"
  marker=""
  if [ -n "$detect_cmd" ] && command -v "$detect_cmd" &>/dev/null; then
    marker=" ${GREEN}●${NC}"
  fi
  echo -e "    ${CYAN}$i)${NC} $label$marker"
  (( i++ ))
done
echo -e "    ${CYAN}a)${NC} All of the above"
echo ""
echo -e "  ${DIM}● = detected on this machine${NC}"
echo ""
read -rp "  Choice (e.g. 1, 1 3, a): " choice
echo ""

# Parse selection into indices (0-based)
selected=()
if [[ "$choice" == "a" || "$choice" == "all" ]]; then
  for (( j=0; j<${#AGENTS[@]}; j++ )); do selected+=("$j"); done
else
  for token in $choice; do
    if [[ "$token" =~ ^[0-9]+$ ]] && (( token >= 1 && token <= ${#AGENTS[@]} )); then
      selected+=("$(( token - 1 ))")
    fi
  done
fi

if [ ${#selected[@]} -eq 0 ]; then
  echo -e "  ${YELLOW}No valid selection — exiting.${NC}"
  exit 1
fi

# ── Install each selected agent ──────────────────────────
install_agent() {
  local label="$1" skill_src="$2" skills_dst="$3" data_dir="$4"
  local src_path="$SCRIPT_DIR/$skill_src"

  echo -e "${CYAN}── $label ${DIM}────────────────────────────────────────${NC}"
  echo ""

  if [ ! -d "$src_path" ]; then
    echo -e "  ${YELLOW}⚠${NC}  No skills found at $skill_src — skipping."
    echo ""
    return
  fi

  mkdir -p "$skills_dst" "$data_dir"

  # Install skills
  echo -e "  ${DIM}Installing skills...${NC}"
  for skill_src_dir in "$src_path"/*/; do
    skill_name=$(basename "$skill_src_dir")
    target="$skills_dst/$skill_name"
    rm -rf "$target"
    cp -r "$skill_src_dir" "$target"
    slash_cmd=$(grep -m1 '^name:' "$target/SKILL.md" | sed 's/name: *//')
    echo -e "    ${GREEN}✓${NC} /${slash_cmd}"
  done

  # Bootstrap user data
  echo ""
  echo -e "  ${DIM}User data (${data_dir})...${NC}"
  if [ ! -f "$data_dir/config.md" ]; then
    cp "$SCRIPT_DIR/data/config.md" "$data_dir/config.md"
    echo -e "    ${GREEN}✓${NC} config.md ${DIM}(new — edit your vault path!)${NC}"
  else
    echo -e "    ${YELLOW}→${NC} config.md ${DIM}(preserved)${NC}"
  fi
  if [ ! -f "$data_dir/brain-rules.md" ]; then
    cp "$SCRIPT_DIR/data/brain-rules.md" "$data_dir/brain-rules.md"
    echo -e "    ${GREEN}✓${NC} brain-rules.md ${DIM}(new)${NC}"
  else
    echo -e "    ${YELLOW}→${NC} brain-rules.md ${DIM}(preserved)${NC}"
  fi
  echo ""
}

for idx in "${selected[@]}"; do
  IFS='|' read -r label skill_src skills_dst data_dir _ <<< "${AGENTS[$idx]}"
  install_agent "$label" "$skill_src" "$skills_dst" "$data_dir"
done

# ── kepano companion (Claude Code only) ─────────────────
for idx in "${selected[@]}"; do
  IFS='|' read -r label _ _ _ detect_cmd <<< "${AGENTS[$idx]}"
  if [[ "$label" == "Claude Code" ]]; then
    claude_skills_dst="$HOME/.claude/skills"
    echo -e "${CYAN}── kepano's obsidian-skills ${DIM}(Claude Code companion)${NC}${CYAN} ────${NC}"
    echo ""
    if command -v git &>/dev/null; then
      TEMP=$(mktemp -d)
      if git clone --depth=1 --quiet https://github.com/kepano/obsidian-skills.git "$TEMP" 2>/dev/null; then
        for skill_dir in "$TEMP/skills/"*/; do
          kep_name=$(basename "$skill_dir")
          if [ -d "$skill_dir" ] && [ ! -d "$claude_skills_dst/$kep_name" ]; then
            cp -r "$skill_dir" "$claude_skills_dst/$kep_name"
            echo -e "    ${GREEN}✓${NC} $kep_name"
          else
            echo -e "    ${YELLOW}→${NC} $kep_name ${DIM}(already installed)${NC}"
          fi
        done
        rm -rf "$TEMP"
      else
        echo -e "    ${YELLOW}⚠${NC}  Clone failed — install manually:"
        echo -e "    ${DIM}cp -r obsidian-skills/skills/* ~/.claude/skills/${NC}"
      fi
    else
      echo -e "    ${YELLOW}⚠${NC}  git not found — skipping"
    fi
    echo ""
    break
  fi
done

# ── Summary ──────────────────────────────────────────────
echo -e "${GREEN}┌──────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│          ✅  Installation complete!       │${NC}"
echo -e "${GREEN}└──────────────────────────────────────────┘${NC}"
echo ""
echo "  Next steps:"
echo ""
for idx in "${selected[@]}"; do
  IFS='|' read -r label _ _ data_dir _ <<< "${AGENTS[$idx]}"
  echo -e "  ${CYAN}$label${NC}"
  echo -e "    Edit vault path: ${DIM}$data_dir/config.md${NC}"
  echo ""
done
echo -e "  ${DIM}Re-run setup.sh anytime — config and rules are always preserved.${NC}"
echo ""
