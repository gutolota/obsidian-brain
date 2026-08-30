#!/usr/bin/env python3
"""Local no-cost Obsidian knowledge index: FTS5 + vectors + graph."""
from __future__ import annotations

import argparse
import array
import datetime as dt
import hashlib
import json
import math
import re
import sqlite3
from pathlib import Path

HASH_DIM = 1024
DEFAULT_EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9_-]{2,}")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(r"(?<![\w/])#([\wÀ-ÿ][\wÀ-ÿ/-]*)", re.UNICODE)
EXCLUDED = {
    ".obsidian", ".git", ".trash", ".venv", "venv", "node_modules",
    "Templates", "Sistema", "analysis_outputs",
}
SENSITIVE_NAME_RE = re.compile(r"(?:senha|password|passwd|credential|secret|token|api[ _-]?key|private[ _-]?key|account)", re.IGNORECASE)
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


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5 :]
    return text


def title_from(text: str, fallback: str) -> str:
    body = strip_frontmatter(text)
    match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def tokens(text: str) -> list[str]:
    words = [w.casefold() for w in WORD_RE.findall(text)]
    features = list(words)
    for word in words:
        padded = f"^{word}$"
        features.extend(padded[i : i + 3] for i in range(max(0, len(padded) - 2)))
    return features


def hash_vectorize(text: str) -> array.array:
    vec = array.array("f", [0.0]) * HASH_DIM
    for token in tokens(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "little")
        index = value % HASH_DIM
        sign = 1.0 if value & (1 << 63) else -1.0
        vec[index] += sign
    norm = math.sqrt(sum(x * x for x in vec))
    if norm:
        for i in range(HASH_DIM):
            vec[i] /= norm
    return vec


def embed_texts(texts: list[str], backend: str, model_name: str) -> tuple[list[array.array], int]:
    if backend == "fastembed":
        try:
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise SystemExit("fastembed is required for neural embeddings; install it or use --backend hash") from exc
        model = TextEmbedding(model_name=model_name)
        vectors = []
        for vector in model.embed(texts, batch_size=16):
            values = array.array("f", vector.tolist())
            norm = math.sqrt(sum(x * x for x in values))
            if norm:
                values = array.array("f", (x / norm for x in values))
            vectors.append(values)
        return vectors, len(vectors[0]) if vectors else 0
    vectors = [hash_vectorize(text) for text in texts]
    return vectors, HASH_DIM


def cosine_blob(query: array.array, blob: bytes) -> float:
    candidate = array.array("f")
    candidate.frombytes(blob)
    if len(candidate) != len(query):
        return 0.0
    return sum(a * b for a, b in zip(query, candidate))


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    con.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            folder TEXT NOT NULL,
            mtime REAL NOT NULL,
            body TEXT NOT NULL,
            tags TEXT NOT NULL,
            vector BLOB NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
            title, body, tags, content='notes', content_rowid='id',
            tokenize='unicode61 remove_diacritics 2'
        );
        CREATE TABLE IF NOT EXISTS edges (
            source_id INTEGER NOT NULL,
            target_title TEXT NOT NULL,
            relation TEXT NOT NULL DEFAULT 'wikilink',
            UNIQUE(source_id, target_title, relation)
        );
        CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
        CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_title);
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """
    )
    return con


def markdown_files(vault: Path):
    for path in vault.rglob("*.md"):
        parts = path.relative_to(vault).parts
        if any(part in EXCLUDED for part in parts):
            continue
        if SENSITIVE_NAME_RE.search(path.stem):
            continue
        if path.is_file():
            yield path


def rebuild(vault: Path, db: Path, backend: str, model_name: str) -> dict:
    con = connect(db)
    con.execute("DELETE FROM edges")
    con.execute("DELETE FROM notes_fts")
    con.execute("DELETE FROM notes")
    records = []
    embedding_inputs = []
    for path in markdown_files(vault):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            mtime = path.stat().st_mtime
        except (FileNotFoundError, OSError):
            continue
        if SENSITIVE_CONTENT_RE.search(text):
            continue
        body = strip_frontmatter(text)
        rel = path.relative_to(vault).as_posix()
        title = title_from(text, path.stem)
        tags = sorted(set(TAG_RE.findall(text)))
        records.append((path, rel, title, tags, body, mtime))
        embedding_inputs.append(f"{title}\n{' '.join(tags)}\n{body[:12000]}")
    vectors, dimensions = embed_texts(embedding_inputs, backend, model_name)
    edges = 0
    for (path, rel, title, tags, body, mtime), vec in zip(records, vectors):
        cur = con.execute(
            "INSERT INTO notes(path,title,folder,mtime,body,tags,vector) VALUES(?,?,?,?,?,?,?)",
            (rel, title, str(Path(rel).parent), mtime, body, json.dumps(tags, ensure_ascii=False), vec.tobytes()),
        )
        note_id = cur.lastrowid
        con.execute(
            "INSERT INTO notes_fts(rowid,title,body,tags) VALUES(?,?,?,?)",
            (note_id, title, body, " ".join(tags)),
        )
        for target in sorted(set(LINK_RE.findall(body))):
            con.execute("INSERT OR IGNORE INTO edges(source_id,target_title) VALUES(?,?)", (note_id, target.strip()))
            edges += 1
    generated = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    metadata = {
        "generated": generated,
        "vault": str(vault),
        "embedding_backend": backend,
        "embedding_model": model_name if backend == "fastembed" else "deterministic-hash",
        "embedding_dimensions": str(dimensions),
    }
    for key, value in metadata.items():
        con.execute("INSERT OR REPLACE INTO metadata(key,value) VALUES(?,?)", (key, value))
    con.commit()
    con.close()
    return {"notes": len(records), "edges": edges, "database": str(db), **metadata}


def safe_fts_query(query: str) -> str:
    words = [w for w in WORD_RE.findall(query) if len(w) >= 3]
    return " OR ".join(f'"{w.replace(chr(34), "")}"' for w in words[:12])


def snippet(body: str, query: str, limit: int = 280) -> str:
    compact = re.sub(r"\s+", " ", body).strip()
    positions = [compact.casefold().find(w.casefold()) for w in WORD_RE.findall(query)]
    positions = [p for p in positions if p >= 0]
    start = max(0, (min(positions) if positions else 0) - 80)
    result = compact[start : start + limit]
    return ("…" if start else "") + result + ("…" if start + limit < len(compact) else "")


def search(db: Path, query: str, limit: int) -> dict:
    con = connect(db)
    backend_row = con.execute("SELECT value FROM metadata WHERE key='embedding_backend'").fetchone()
    model_row = con.execute("SELECT value FROM metadata WHERE key='embedding_model'").fetchone()
    backend = backend_row[0] if backend_row else "hash"
    model_name = model_row[0] if model_row and backend == "fastembed" else DEFAULT_EMBED_MODEL
    qvec = embed_texts([query], backend, model_name)[0][0]
    vector_rows = con.execute("SELECT id,path,title,folder,body,vector FROM notes").fetchall()
    vector_scores = {row["id"]: max(0.0, cosine_blob(qvec, row["vector"])) for row in vector_rows}
    fts_scores: dict[int, float] = {}
    fts_query = safe_fts_query(query)
    if fts_query:
        try:
            rows = con.execute(
                "SELECT rowid, bm25(notes_fts, 4.0, 1.0, 2.0) AS rank FROM notes_fts WHERE notes_fts MATCH ? LIMIT 100",
                (fts_query,),
            ).fetchall()
            for row in rows:
                fts_scores[row["rowid"]] = 1.0 / (1.0 + max(0.0, row["rank"] + 10.0))
        except sqlite3.OperationalError:
            pass
    scored = []
    for row in vector_rows:
        fts = fts_scores.get(row["id"], 0.0)
        vec = vector_scores[row["id"]]
        score = 0.65 * vec + 0.35 * fts
        if score > 0:
            scored.append((score, vec, fts, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for score, vec, fts, row in scored[:limit]:
        results.append({
            "path": row["path"],
            "title": row["title"],
            "score": round(score, 4),
            "vector_score": round(vec, 4),
            "fts_score": round(fts, 4),
            "snippet": snippet(row["body"], query),
        })
    generated_row = con.execute("SELECT value FROM metadata WHERE key='generated'").fetchone()
    vault_row = con.execute("SELECT value FROM metadata WHERE key='vault'").fetchone()
    vault_path = Path(vault_row[0]) if vault_row else None
    if vault_path:
        for result in results:
            result["absolute_path"] = str(vault_path / result["path"])
    con.close()
    return {
        "query": query,
        "generated": generated_row[0] if generated_row else None,
        "vault": str(vault_path) if vault_path else None,
        "results": results,
    }


def related(db: Path, note_query: str, limit: int) -> dict:
    con = connect(db)
    row = con.execute(
        "SELECT * FROM notes WHERE path=? OR title=? OR path LIKE ? ORDER BY length(path) LIMIT 1",
        (note_query, note_query, f"%{note_query}%"),
    ).fetchone()
    if not row:
        con.close()
        return {"error": "note not found", "query": note_query, "results": []}
    qvec = array.array("f")
    qvec.frombytes(row["vector"])
    candidates = con.execute("SELECT id,path,title,body,vector FROM notes WHERE id != ?", (row["id"],)).fetchall()
    scores = sorted(
        ((cosine_blob(qvec, candidate["vector"]), candidate) for candidate in candidates),
        key=lambda x: x[0], reverse=True,
    )[:limit]
    outgoing = [r[0] for r in con.execute("SELECT target_title FROM edges WHERE source_id=?", (row["id"],))]
    incoming = [dict(r) for r in con.execute(
        "SELECT n.path,n.title FROM edges e JOIN notes n ON n.id=e.source_id WHERE lower(e.target_title)=lower(?) OR lower(e.target_title)=lower(?)",
        (row["title"], Path(row["path"]).stem),
    )]
    con.close()
    return {
        "note": {"path": row["path"], "title": row["title"]},
        "outgoing": outgoing,
        "incoming": incoming,
        "similar": [
            {"path": candidate["path"], "title": candidate["title"], "score": round(score, 4)}
            for score, candidate in scores
        ],
    }


def stats(db: Path) -> dict:
    con = connect(db)
    notes = con.execute("SELECT count(*) FROM notes").fetchone()[0]
    edges = con.execute("SELECT count(*) FROM edges").fetchone()[0]
    folders = [dict(row) for row in con.execute("SELECT folder,count(*) AS count FROM notes GROUP BY folder ORDER BY count DESC LIMIT 20")]
    metadata = {row["key"]: row["value"] for row in con.execute("SELECT key,value FROM metadata")}
    con.close()
    return {"notes": notes, "edges": edges, **metadata, "folders": folders}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    p_build = sub.add_parser("build")
    p_build.add_argument("vault", type=Path)
    p_build.add_argument("--backend", choices=["fastembed", "hash"], default="fastembed")
    p_build.add_argument("--model", default=DEFAULT_EMBED_MODEL)
    p_search = sub.add_parser("search")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=8)
    p_related = sub.add_parser("related")
    p_related.add_argument("note")
    p_related.add_argument("--limit", type=int, default=8)
    sub.add_parser("stats")
    args = parser.parse_args()
    db = args.db.expanduser().resolve()
    if args.command == "build":
        vault = args.vault.expanduser().resolve()
        if not vault.is_dir():
            raise SystemExit(f"Vault not found: {vault}")
        result = rebuild(vault, db, args.backend, args.model)
    elif args.command == "search":
        result = search(db, args.query, max(1, min(args.limit, 50)))
    elif args.command == "related":
        result = related(db, args.note, max(1, min(args.limit, 50)))
    else:
        result = stats(db)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
