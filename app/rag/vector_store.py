import os
import sqlite3
import sqlite_vec
from openai import OpenAI
from app.common.logger import logger


class RecipeVectorStore:
    """Local recipe knowledge base using sqlite-vec + DashScope embeddings."""

    EMBEDDING_MODEL = "text-embedding-v4"
    EMBEDDING_DIM = 1024
    TOP_K_DEFAULT = 5

    def __init__(self, db_path: str, base_url: str, api_key: str):
        self.db_path = db_path
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.enable_load_extension(True)
            sqlite_vec.load(self._conn)
            self._conn.row_factory = sqlite3.Row
            self._create_tables()
        return self._conn

    def _create_tables(self):
        self.conn.executescript("""
            CREATE VIRTUAL TABLE IF NOT EXISTS recipe_embeddings USING vec0(
                embedding float[1024]
            );
            CREATE TABLE IF NOT EXISTS recipe_metadata (
                rowid INTEGER PRIMARY KEY,
                id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                ingredients TEXT,
                cuisine TEXT,
                difficulty TEXT,
                cooking_time INTEGER,
                nutrition TEXT,
                steps TEXT,
                tags TEXT
            );
        """)

    def _embed(self, texts: list[str]) -> list[list[float]]:
        # DashScope limits batch size to 10
        BATCH_SIZE = 10
        all_embeddings = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            resp = self.client.embeddings.create(model=self.EMBEDDING_MODEL, input=batch)
            all_embeddings.extend(d.embedding for d in resp.data)
        return all_embeddings

    @staticmethod
    def _embed_text(recipe: dict) -> str:
        return (
            f"Recipe: {recipe['name']}. "
            f"Ingredients: {recipe['ingredients']}. "
            f"Cuisine: {recipe['cuisine']}. "
            f"Difficulty: {recipe['difficulty']}. "
            f"Tags: {recipe['tags']}. "
            f"Nutrition: {recipe['nutrition']}."
        )

    def count(self) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) as cnt FROM recipe_metadata"
        ).fetchone()
        return row["cnt"] if row else 0

    def seed(self, recipes: list[dict]) -> int:
        """Embed and insert all recipes. Returns count of newly inserted recipes."""
        if not recipes:
            return 0

        existing_ids = {
            r["id"] for r in
            self.conn.execute("SELECT id FROM recipe_metadata").fetchall()
        }
        new_recipes = [r for r in recipes if r["id"] not in existing_ids]
        if not new_recipes:
            logger.info("All seed recipes already indexed. Skipping.")
            return 0

        texts = [self._embed_text(r) for r in new_recipes]
        embeddings = self._embed(texts)

        for recipe, emb in zip(new_recipes, embeddings):
            emb_json = str(emb)  # [0.1, 0.2, ...] as JSON string
            self.conn.execute(
                "INSERT INTO recipe_embeddings (embedding) VALUES (?)",
                [emb_json]
            )
            rowid = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self.conn.execute(
                """INSERT INTO recipe_metadata
                   (rowid, id, name, ingredients, cuisine, difficulty,
                    cooking_time, nutrition, steps, tags)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    rowid,
                    recipe["id"], recipe["name"], recipe["ingredients"],
                    recipe["cuisine"], recipe["difficulty"],
                    recipe.get("cooking_time", 0),
                    recipe["nutrition"], recipe["steps"], recipe["tags"]
                )
            )

        self.conn.commit()
        logger.info(f"Seeded {len(new_recipes)} recipes into RAG knowledge base.")
        return len(new_recipes)

    def search(self, query: str, top_k: int = TOP_K_DEFAULT) -> list[dict]:
        """Search recipes by semantic similarity to the query."""
        [query_vec] = self._embed([query])
        query_json = str(query_vec)

        rows = self.conn.execute(
            """SELECT m.id, m.name, m.ingredients, m.cuisine, m.difficulty,
                      m.cooking_time, m.nutrition, m.steps, m.tags,
                      distance
               FROM recipe_embeddings e
               JOIN recipe_metadata m ON e.rowid = m.rowid
               WHERE e.embedding MATCH ? AND k = ?
               ORDER BY distance ASC""",
            [query_json, top_k]
        ).fetchall()

        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "name": row["name"],
                "ingredients": row["ingredients"],
                "cuisine": row["cuisine"],
                "difficulty": row["difficulty"],
                "cooking_time": row["cooking_time"],
                "nutrition": row["nutrition"],
                "steps": row["steps"],
                "tags": row["tags"],
                "distance": round(row["distance"], 4)
            })
        return results

    def add_recipe(self, recipe: dict) -> bool:
        """Add a single recipe to the knowledge base."""
        existing = self.conn.execute(
            "SELECT 1 FROM recipe_metadata WHERE id = ?", [recipe["id"]]
        ).fetchone()
        if existing:
            logger.warning(f"Recipe {recipe['id']} already exists. Skipping.")
            return False

        text = self._embed_text(recipe)
        [emb] = self._embed([text])

        self.conn.execute(
            "INSERT INTO recipe_embeddings (embedding) VALUES (?)",
            [str(emb)]
        )
        rowid = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        self.conn.execute(
            """INSERT INTO recipe_metadata
               (rowid, id, name, ingredients, cuisine, difficulty,
                cooking_time, nutrition, steps, tags)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (rowid, recipe["id"], recipe["name"], recipe["ingredients"],
             recipe["cuisine"], recipe["difficulty"],
             recipe.get("cooking_time", 0),
             recipe["nutrition"], recipe["steps"], recipe["tags"])
        )
        self.conn.commit()
        logger.info(f"Added recipe '{recipe['name']}' to knowledge base.")
        return True

    def delete_recipe(self, recipe_id: str) -> bool:
        """Remove a recipe by its ID."""
        row = self.conn.execute(
            "SELECT rowid FROM recipe_metadata WHERE id = ?", [recipe_id]
        ).fetchone()
        if not row:
            return False
        rid = row["rowid"]
        self.conn.execute("DELETE FROM recipe_metadata WHERE rowid = ?", [rid])
        self.conn.execute("DELETE FROM recipe_embeddings WHERE rowid = ?", [rid])
        self.conn.commit()
        logger.info(f"Deleted recipe '{recipe_id}' from knowledge base.")
        return True

    def update_recipe(self, recipe_id: str, recipe: dict) -> bool:
        """Update a recipe: delete old entry, then re-add with fresh embedding."""
        if not self.delete_recipe(recipe_id):
            return False
        return self.add_recipe(recipe)

    def rebuild(self, recipes: list[dict]) -> None:
        """Drop and recreate tables, then re-seed with given recipes."""
        self.conn.execute("DROP TABLE IF EXISTS recipe_embeddings")
        self.conn.execute("DROP TABLE IF EXISTS recipe_metadata")
        self._conn.commit()
        self._create_tables()
        count = self.seed(recipes)
        logger.info(f"Rebuilt knowledge base: {count} recipes indexed.")

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
