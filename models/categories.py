"""Category model queries."""

import sqlite3


def get_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return all categories ordered by type then name."""
    return db.execute(
        "SELECT id, name, type FROM categories ORDER BY type, name"
    ).fetchall()


def get_by_type(db: sqlite3.Connection, cat_type: str) -> list[sqlite3.Row]:
    """Return categories filtered by type."""
    return db.execute(
        "SELECT id, name, type FROM categories WHERE type = ? ORDER BY name",
        (cat_type,),
    ).fetchall()


def get_grouped(db: sqlite3.Connection) -> dict[str, list[sqlite3.Row]]:
    """Return categories grouped by type."""
    all_cats = get_all(db)
    grouped: dict[str, list[sqlite3.Row]] = {
        "fixed": [],
        "variable": [],
        "extra": [],
    }
    for cat in all_cats:
        grouped[cat["type"]].append(cat)
    return grouped


def get_by_id(db: sqlite3.Connection, cat_id: int) -> sqlite3.Row | None:
    """Return a category by ID."""
    return db.execute(
        "SELECT id, name, type FROM categories WHERE id = ?", (cat_id,)
    ).fetchone()


def create(db: sqlite3.Connection, name: str, cat_type: str) -> int | None:
    """Create a new category. Returns the ID or None on duplicate."""
    try:
        cursor = db.execute(
            "INSERT INTO categories (name, type) VALUES (?, ?)",
            (name, cat_type),
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def update(db: sqlite3.Connection, cat_id: int, name: str, cat_type: str) -> bool:
    """Update a category. Returns False on duplicate name."""
    try:
        db.execute(
            "UPDATE categories SET name = ?, type = ? WHERE id = ?",
            (name, cat_type, cat_id),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def is_in_use(db: sqlite3.Connection, cat_id: int) -> bool:
    """Check if a category is referenced by any expenses or budget entries."""
    row = db.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM expected_expenses WHERE category_id = ?
            UNION ALL
            SELECT 1 FROM actual_expenses WHERE category_id = ?
        ) AS used
        """,
        (cat_id, cat_id),
    ).fetchone()
    return bool(row["used"])


def delete(db: sqlite3.Connection, cat_id: int) -> bool:
    """Delete a category. Returns False if it's in use."""
    if is_in_use(db, cat_id):
        return False
    db.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
    db.commit()
    return True
