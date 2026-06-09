import sqlite3, json, os
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)

# In production (Render), data lives on a persistent disk at /data
# Locally it lives next to app.py
_data_dir = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
DB_PATH   = os.path.join(_data_dir, "questions.db")

# ── DB helpers ─────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exc=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS questions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            q          TEXT    NOT NULL,
            type       TEXT    NOT NULL CHECK(type IN ('mcq','theory','practical','technical')),
            company    TEXT    DEFAULT '',
            date       TEXT    DEFAULT '',
            round      TEXT    DEFAULT '',
            ans        TEXT    DEFAULT '',
            tags       TEXT    DEFAULT '[]',
            options    TEXT    DEFAULT '[]',
            correct    INTEGER DEFAULT -1,
            marked     INTEGER DEFAULT 0,
            created_at TEXT    DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_type    ON questions(type);
        CREATE INDEX IF NOT EXISTS idx_company ON questions(company);
        CREATE INDEX IF NOT EXISTS idx_marked  ON questions(marked);
    """)
    db.commit()
    db.close()

def row_to_dict(row):
    d = dict(row)
    d["tags"]    = json.loads(d.get("tags")    or "[]")
    d["options"] = json.loads(d.get("options") or "[]")
    d["marked"]  = bool(d.get("marked", 0))
    return d

# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/questions", methods=["GET"])
def get_questions():
    rows = get_db().execute(
        "SELECT * FROM questions ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/questions", methods=["POST"])
def add_question():
    d = request.json
    cur = get_db().execute(
        """INSERT INTO questions
               (q, type, company, date, round, ans, tags, options, correct, marked)
           VALUES (?,?,?,?,?,?,?,?,?,0)""",
        (d.get("q",""), d.get("type","mcq"), d.get("company",""),
         d.get("date",""), d.get("round",""), d.get("ans",""),
         json.dumps(d.get("tags",[])), json.dumps(d.get("options",[])),
         d.get("correct",-1))
    )
    get_db().commit()
    row = get_db().execute("SELECT * FROM questions WHERE id=?",
                           (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201

@app.route("/api/questions/<int:qid>", methods=["PUT"])
def update_question(qid):
    d  = request.json
    db = get_db()
    db.execute(
        """UPDATE questions SET q=?, type=?, company=?, date=?, round=?,
               ans=?, tags=?, options=?, correct=?
           WHERE id=?""",
        (d.get("q",""), d.get("type","mcq"), d.get("company",""),
         d.get("date",""), d.get("round",""), d.get("ans",""),
         json.dumps(d.get("tags",[])), json.dumps(d.get("options",[])),
         d.get("correct",-1), qid)
    )
    db.commit()
    row = db.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row_to_dict(row))

@app.route("/api/questions/<int:qid>", methods=["DELETE"])
def delete_question(qid):
    db = get_db()
    db.execute("DELETE FROM questions WHERE id=?", (qid,))
    db.commit()
    return jsonify({"ok": True})

@app.route("/api/questions/<int:qid>/bookmark", methods=["POST"])
def toggle_bookmark(qid):
    db = get_db()
    db.execute("UPDATE questions SET marked = NOT marked WHERE id=?", (qid,))
    db.commit()
    row = db.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row_to_dict(row))

@app.route("/api/stats")
def stats():
    db    = get_db()
    rows  = db.execute("SELECT type, COUNT(*) cnt FROM questions GROUP BY type").fetchall()
    total = db.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    bm    = db.execute("SELECT COUNT(*) FROM questions WHERE marked=1").fetchone()[0]
    return jsonify({"total": total, "marked": bm,
                    "by_type": {r["type"]: r["cnt"] for r in rows}})

init_db()
# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n✅  Interview Question Bank is running!")
    print(f"   Database : {DB_PATH}")
    print("   Open     : http://127.0.0.1:5000\n")
    app.run(debug=True)
