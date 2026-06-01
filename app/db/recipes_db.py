import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "personal_chief.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            cuisine TEXT NOT NULL DEFAULT 'Western',
            difficulty TEXT NOT NULL DEFAULT 'easy',
            cooking_time INTEGER NOT NULL DEFAULT 0,
            nutrition TEXT NOT NULL DEFAULT '',
            steps TEXT NOT NULL DEFAULT '',
            tags TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def list_all(cuisine: str = None, difficulty: str = None,
             search: str = None, limit: int = 50, offset: int = 0) -> list[dict]:
    conn = get_conn()
    clauses = []
    params = []
    if cuisine:
        clauses.append("cuisine = ?")
        params.append(cuisine)
    if difficulty:
        clauses.append("difficulty = ?")
        params.append(difficulty)
    if search:
        clauses.append("(name LIKE ? OR ingredients LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    query = f"SELECT * FROM recipes{where} ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_by_id(recipe_id: str) -> dict | None:
    conn = get_conn()
    row = conn.execute("SELECT * FROM recipes WHERE id = ?", [recipe_id]).fetchone()
    conn.close()
    return dict(row) if row else None


def insert(recipe: dict) -> bool:
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO recipes (id, name, ingredients, cuisine, difficulty,
                                 cooking_time, nutrition, steps, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            recipe["id"], recipe["name"], recipe["ingredients"],
            recipe.get("cuisine", "Western"), recipe.get("difficulty", "easy"),
            recipe.get("cooking_time", 0), recipe.get("nutrition", ""),
            recipe.get("steps", ""), recipe.get("tags", "")
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update(recipe_id: str, recipe: dict) -> bool:
    conn = get_conn()
    existing = conn.execute("SELECT * FROM recipes WHERE id = ?", [recipe_id]).fetchone()
    if not existing:
        conn.close()
        return False

    fields = []
    params = []
    for key in ["name", "ingredients", "cuisine", "difficulty",
                "cooking_time", "nutrition", "steps", "tags"]:
        if key in recipe:
            fields.append(f"{key} = ?")
            params.append(recipe[key])
    if not fields:
        conn.close()
        return False

    fields.append("updated_at = datetime('now')")
    params.append(recipe_id)
    conn.execute(f"UPDATE recipes SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    return True


def delete(recipe_id: str) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM recipes WHERE id = ?", [recipe_id])
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def count() -> int:
    conn = get_conn()
    row = conn.execute("SELECT COUNT(*) as cnt FROM recipes").fetchone()
    conn.close()
    return row["cnt"] if row else 0


def seed_from_dicts(recipes: list[dict]) -> int:
    cnt = 0
    for r in recipes:
        if insert(r):
            cnt += 1
    return cnt


def get_all_as_dicts() -> list[dict]:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM recipes ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]
