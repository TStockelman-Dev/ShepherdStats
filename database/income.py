import sqlite3
from typing import List, Optional, Dict, Any

from .connection import get_connection


def add_income(date: str, amount: float, category: str, note: Optional[str] = None, conn: sqlite3.Connection | None = None) -> int:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute(
            "INSERT INTO income (date, amount, category, note) VALUES (?, ?, ?, ?)",
            (date, amount, category, note),
        )
        if close:
            conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not add income record: {e}")
    finally:
        if close:
            conn.close()


def delete_income_by_id(record_id: int, conn: sqlite3.Connection | None = None) -> None:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        conn.execute("DELETE FROM income WHERE id = ?", (record_id,))
        if close:
            conn.commit()
    finally:
        if close:
            conn.close()


def update_income(record_id: int, *, date: Optional[str] = None, amount: Optional[float] = None, category: Optional[str] = None, note: Optional[str] = None, conn: sqlite3.Connection | None = None) -> None:
    fields: List[str] = []
    params: List[Any] = []
    if date is not None:
        fields.append("date = ?")
        params.append(date)
    if amount is not None:
        fields.append("amount = ?")
        params.append(amount)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if note is not None:
        fields.append("note = ?")
        params.append(note)

    if not fields:
        return

    params.append(record_id)
    sql = f"UPDATE income SET {', '.join(fields)} WHERE id = ?"

    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        conn.execute(sql, tuple(params))
        if close:
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not update income record: {e}")
    finally:
        if close:
            conn.close()


def get_income_by_id(record_id: int, conn: sqlite3.Connection | None = None) -> Optional[Dict[str, Any]]:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute("SELECT * FROM income WHERE id = ?", (record_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        if close:
            conn.close()


def get_all_income(conn: sqlite3.Connection | None = None) -> List[Dict[str, Any]]:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute("SELECT * FROM income ORDER BY date DESC, category")
        return [dict(r) for r in cur.fetchall()]
    finally:
        if close:
            conn.close()


def find_income(date: Optional[str] = None, category: Optional[str] = None, conn: sqlite3.Connection | None = None) -> List[Dict[str, Any]]:
    clauses: List[str] = []
    params: List[Any] = []
    if date is not None:
        clauses.append("date = ?")
        params.append(date)
    if category is not None:
        clauses.append("category = ?")
        params.append(category)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT * FROM income {where} ORDER BY date DESC, category"

    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute(sql, tuple(params))
        return [dict(r) for r in cur.fetchall()]
    finally:
        if close:
            conn.close()


__all__ = [
    "add_income",
    "delete_income_by_id",
    "update_income",
    "get_income_by_id",
    "get_all_income",
    "find_income",
]
