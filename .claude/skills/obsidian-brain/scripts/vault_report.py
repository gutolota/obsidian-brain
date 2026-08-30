#!/usr/bin/env python3
"""Generate non-destructive Obsidian vault inventory and review reports."""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

EXCLUDED_PARTS = {
    ".obsidian", ".git", ".trash", ".venv", "venv", "node_modules",
    "Templates", "Sistema", "analysis_outputs",
}
SENSITIVE_NAME_RE = re.compile(
    r"(?:senha|password|passwd|credential|secret|token|api[ _-]?key|private[ _-]?key|account)",
    re.IGNORECASE,
)
SENSITIVE_CONTENT_RE = re.compile(
    r"(?:"
    r"BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY|"
    r"visibility:\s*(?:private|secret)|type:\s*credential|"
    r"^\s*(?:senha|password|passwd|psswd|username|login|user|token|access[_ -]?token|"
    r"refresh[_ -]?token|client[_ -]?secret|api[ _-]?key|private[ _-]?key|x-api-key)\b"
    r".{0,80}[:=]\s*\S+|"
    r"^\s*authorization\s*:\s*(?:bearer|basic)\s+\S+|"
    r"\b(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{30,}|AIza[0-9A-Za-z_-]{30,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}|sk-[A-Za-z0-9_-]{20,}|"
    r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b|"
    r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s/:]+:[^\s/@]+@"
    r")",
    re.IGNORECASE | re.MULTILINE,
)
RAW_DEFAULT = "1 - Notas brutas"
COMPLETE_DEFAULT = "3 - Notas completas"
SYSTEM_DEFAULT = "Sistema"
TASK_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.+?)\s*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(r"(?<![\w/])#([\wÀ-ÿ][\wÀ-ÿ/-]*)", re.UNICODE)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9_-]{3,}")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STOPWORDS = {
    "para", "como", "mais", "isso", "essa", "esse", "uma", "com", "sem", "dos", "das",
    "que", "por", "the", "and", "from", "this", "with", "have", "sobre", "entre", "também",
    "ser", "são", "não", "nos", "nas", "aos", "ainda", "nota", "notas", "projeto", "deve",
    "pode", "cada", "onde", "quando", "qual", "quais", "foi", "está", "sua", "seu", "seus",
}


@dataclass
class Note:
    path: str
    title: str
    folder: str
    mtime: str
    size: int
    note_type: str
    status: str
    tags: list[str]
    wikilinks: list[str]
    open_tasks: list[str]
    done_tasks: list[str]
    word_count: int


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        return [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
    return value.strip("'\"")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    data: dict[str, object] = {}
    current_list: str | None = None
    for line in raw.splitlines():
        if re.match(r"^\s+-\s+", line) and current_list:
            item = re.sub(r"^\s+-\s+", "", line).strip().strip("'\"")
            values = data.setdefault(current_list, [])
            if isinstance(values, list):
                values.append(item)
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        parsed = parse_scalar(value)
        data[key] = [] if value == "" else parsed
        current_list = key if value == "" else None
    return data, text[end + 5 :]


def normalize_tags(frontmatter: dict, body: str) -> list[str]:
    value = frontmatter.get("tags", [])
    if isinstance(value, str):
        tags = [value]
    elif isinstance(value, list):
        tags = [str(x) for x in value]
    else:
        tags = []
    tags.extend(TAG_RE.findall(body))
    return sorted({tag.lstrip("#") for tag in tags if tag})


def scan_note(path: Path, vault: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    open_tasks, done_tasks = [], []
    for line in body.splitlines():
        match = TASK_RE.match(line)
        if not match:
            continue
        (done_tasks if match.group(1).lower() == "x" else open_tasks).append(match.group(2))
    rel = path.relative_to(vault).as_posix()
    return Note(
        path=rel,
        title=path.stem,
        folder=path.parent.relative_to(vault).as_posix(),
        mtime=dt.datetime.fromtimestamp(path.stat().st_mtime).astimezone().isoformat(timespec="seconds"),
        size=path.stat().st_size,
        note_type=str(fm.get("type", "")),
        status=str(fm.get("status", "")),
        tags=normalize_tags(fm, body),
        wikilinks=sorted(set(WIKILINK_RE.findall(body))),
        open_tasks=open_tasks,
        done_tasks=done_tasks,
        word_count=len(WORD_RE.findall(body)),
    )


def iter_markdown(vault: Path) -> Iterable[Path]:
    for path in vault.rglob("*.md"):
        rel_parts = path.relative_to(vault).parts
        if any(part in EXCLUDED_PARTS for part in rel_parts):
            continue
        if SENSITIVE_NAME_RE.search(path.stem):
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if SENSITIVE_CONTENT_RE.search(text):
            continue
        yield path


def wikilink(note: Note) -> str:
    return f"[[{Path(note.path).with_suffix('').as_posix()}|{note.title}]]"


def task_source_link(note: Note) -> str:
    return wikilink(note)


def recent_terms(vault: Path, notes: list[Note], days: int, now: dt.datetime) -> list[tuple[str, int]]:
    cutoff = now - dt.timedelta(days=days)
    counts: collections.Counter[str] = collections.Counter()
    for note in notes:
        when = dt.datetime.fromisoformat(note.mtime)
        if when < cutoff:
            continue
        text = (vault / note.path).read_text(encoding="utf-8", errors="replace")
        _, body = parse_frontmatter(text)
        words = {word.casefold() for word in WORD_RE.findall(body)}
        counts.update(word for word in words if word not in STOPWORDS and not word.isdigit())
    return counts.most_common(20)


def managed_header(title: str, now: dt.datetime) -> str:
    stamp = now.isoformat(timespec="seconds")
    return (
        "---\n"
        f"generated: {stamp}\n"
        "managed_by: obsidian-brain\n"
        "---\n\n"
        f"# {title}\n\n"
        "> [!warning] Arquivo gerenciado automaticamente\n"
        "> Edite a configuração ou a skill, não este relatório. Nenhuma nota-fonte foi alterada.\n\n"
    )


def build_summary(vault: Path, notes: list[Note], now: dt.datetime, raw_folder: str, complete_folder: str) -> str:
    folders = collections.Counter(note.folder.split("/")[0] for note in notes)
    raw = [n for n in notes if n.path.startswith(raw_folder + "/")]
    complete = [n for n in notes if n.path.startswith(complete_folder + "/")]
    open_count = sum(len(n.open_tasks) for n in notes)
    done_count = sum(len(n.done_tasks) for n in notes)
    linked = sum(bool(n.wikilinks) for n in notes)
    out = managed_header("Resumo da vault", now)
    out += "## Visão geral\n\n"
    out += f"- Notas Markdown analisadas: **{len(notes)}**\n"
    out += f"- Notas brutas: **{len(raw)}**\n"
    out += f"- Notas completas: **{len(complete)}**\n"
    out += f"- Tarefas abertas: **{open_count}**\n"
    out += f"- Tarefas concluídas: **{done_count}**\n"
    out += f"- Notas com ao menos um wikilink de saída: **{linked}**\n"
    out += f"- Notas sem wikilinks de saída: **{len(notes) - linked}**\n\n"
    out += "## Pastas principais\n\n| Pasta | Notas |\n|---|---:|\n"
    for folder, count in folders.most_common():
        out += f"| `{folder}` | {count} |\n"
    out += "\n## Observações\n\n"
    out += "- As contagens excluem `.obsidian/`, `Templates/`, `Sistema/` e `analysis_outputs/`.\n"
    out += "- `mtime` pode refletir sincronização ou formatação, não necessariamente atenção renovada.\n"
    return out


def build_tasks(notes: list[Note], now: dt.datetime) -> str:
    out = managed_header("Resumo de tarefas", now)
    out += "## Tarefas abertas\n\n"
    opened = [(n, task) for n in notes for task in n.open_tasks]
    if opened:
        for note, task in opened:
            out += f"- [ ] {task} — {task_source_link(note)}\n"
    else:
        out += "_Nenhuma tarefa aberta encontrada._\n"
    out += "\n## Concluídas registradas\n\n"
    done = [(n, task) for n in notes for task in n.done_tasks]
    if done:
        for note, task in done[-100:]:
            out += f"- [x] {task} — {task_source_link(note)}\n"
    else:
        out += "_Nenhuma tarefa concluída encontrada._\n"
    out += f"\nTotal: **{len(opened)} abertas**, **{len(done)} concluídas**.\n"
    return out


def build_queue(notes: list[Note], now: dt.datetime, raw_folder: str) -> str:
    raw = [n for n in notes if n.path.startswith(raw_folder + "/")]
    candidates = sorted(raw, key=lambda n: n.mtime, reverse=True)
    out = managed_header("Caixa de lapidação", now)
    out += "## Fila dinâmica\n\n"
    out += "```dataview\nTABLE status, file.mtime AS \"Atualizada\", topics AS \"Temas\", projects AS \"Projetos\"\n"
    out += f'FROM "{raw_folder}"\nWHERE type = "fleeting" AND status != "processed" AND status != "archived"\nSORT file.mtime DESC\n```\n\n'
    out += "## Notas recentes sem estado de processamento\n\n"
    missing = [n for n in candidates if not n.status or n.status == "inbox"][:50]
    if missing:
        for note in missing:
            state = note.status or "sem status"
            out += f"- {wikilink(note)} · `{state}` · {note.word_count} palavras · atualizada {note.mtime[:10]}\n"
    else:
        out += "_Nenhuma candidata encontrada._\n"
    return out


def build_radar(vault: Path, notes: list[Note], now: dt.datetime) -> str:
    terms7 = recent_terms(vault, notes, 7, now)
    terms30 = recent_terms(vault, notes, 30, now)
    recent = sorted(notes, key=lambda n: n.mtime, reverse=True)[:25]
    out = managed_header("Radar de pensamentos", now)
    out += "## Sinais quantitativos\n\n"
    out += "> [!info] Interpretação\n> Os termos abaixo indicam recorrência lexical em notas recentes. Não provam importância, intenção ou interesse persistente.\n\n"
    out += "### Termos em notas dos últimos 7 dias\n\n"
    out += ", ".join(f"`{term}` ({count})" for term, count in terms7) or "_Sem dados._"
    out += "\n\n### Termos em notas dos últimos 30 dias\n\n"
    out += ", ".join(f"`{term}` ({count})" for term, count in terms30) or "_Sem dados._"
    out += "\n\n## Evidências recentes\n\n"
    for note in recent:
        out += f"- {wikilink(note)} · atualizada {note.mtime[:10]} · {note.word_count} palavras\n"
    out += "\n## Próxima análise semântica\n\nUse `obsidian-brain:reflect` para transformar estes sinais em hipóteses temáticas citadas.\n"
    return out


def build_weekly(notes: list[Note], now: dt.datetime, raw_folder: str) -> str:
    week_ago = now - dt.timedelta(days=7)
    touched = [n for n in notes if dt.datetime.fromisoformat(n.mtime) >= week_ago]
    open_tasks = [(n, t) for n in notes for t in n.open_tasks]
    done_recent = [(n, t) for n in touched for t in n.done_tasks]
    inbox = [n for n in notes if n.path.startswith(raw_folder + "/") and (not n.status or n.status in {"inbox", "ready"})]
    out = managed_header("Revisão semanal", now)
    out += f"Período observado por modificação: **{week_ago.date()} a {now.date()}**.\n\n"
    out += "## Visão geral\n\n"
    out += f"- Notas tocadas no período: **{len(touched)}**\n- Tarefas abertas: **{len(open_tasks)}**\n"
    out += f"- Tarefas concluídas em notas tocadas: **{len(done_recent)}**\n- Notas brutas em inbox/ready ou sem status: **{len(inbox)}**\n\n"
    out += "## Trabalho registrado\n\n"
    for note in sorted(touched, key=lambda n: n.mtime, reverse=True)[:30]:
        out += f"- {wikilink(note)} · {note.mtime[:10]}\n"
    out += "\n## Próximas decisões do usuário\n\n"
    out += "- [ ] Revisar tarefas abertas no [[Sistema/Resumo de tarefas]].\n"
    out += "- [ ] Selecionar notas para lapidação em [[Sistema/Caixa de lapidação]].\n"
    out += "- [ ] Validar hipóteses no [[Sistema/Radar de pensamentos]].\n"
    out += "\n> [!note] Limite\n> Este relatório não altera tarefas, prioridades, datas ou estados de notas.\n"
    return out


def resolve_managed_folder(vault: Path, system_folder: str) -> Path:
    folder = Path(system_folder)
    if folder.is_absolute() or not system_folder.strip():
        raise ValueError("system folder must be a non-empty relative path inside the vault")
    vault_root = vault.resolve()
    target = (vault_root / folder).resolve()
    try:
        relative = target.relative_to(vault_root)
    except ValueError as exc:
        raise ValueError("system folder escapes the vault") from exc
    if not relative.parts:
        raise ValueError("system folder must not be the vault root")
    return target


def write_reports(vault: Path, reports: dict[str, str], system_folder: str) -> list[str]:
    target = resolve_managed_folder(vault, system_folder)
    target.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in reports.items():
        path = target / name
        path.write_text(content, encoding="utf-8")
        written.append(path.relative_to(vault).as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", type=Path)
    parser.add_argument("--raw-folder", default=RAW_DEFAULT)
    parser.add_argument("--complete-folder", default=COMPLETE_DEFAULT)
    parser.add_argument("--system-folder", default=SYSTEM_DEFAULT)
    parser.add_argument("--write", action="store_true", help="write managed Markdown reports")
    parser.add_argument("--json", dest="json_path", type=Path, help="write inventory JSON")
    args = parser.parse_args()

    vault = args.vault.expanduser().resolve()
    if not vault.is_dir():
        raise SystemExit(f"Vault not found: {vault}")
    now = dt.datetime.now().astimezone()
    notes = [scan_note(path, vault) for path in iter_markdown(vault)]
    notes.sort(key=lambda n: n.path.casefold())

    reports = {
        "Resumo da vault.md": build_summary(vault, notes, now, args.raw_folder, args.complete_folder),
        "Resumo de tarefas.md": build_tasks(notes, now),
        "Caixa de lapidação.md": build_queue(notes, now, args.raw_folder),
        "Radar de pensamentos.md": build_radar(vault, notes, now),
        "Revisão semanal.md": build_weekly(notes, now, args.raw_folder),
    }
    written: list[str] = []
    if args.write:
        try:
            written = write_reports(vault, reports, args.system_folder)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
    if args.json_path:
        payload = {
            "generated": now.isoformat(timespec="seconds"),
            "vault": str(vault),
            "notes": [asdict(n) for n in notes],
        }
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "vault": str(vault),
        "notes": len(notes),
        "open_tasks": sum(len(n.open_tasks) for n in notes),
        "done_tasks": sum(len(n.done_tasks) for n in notes),
        "written": written,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
