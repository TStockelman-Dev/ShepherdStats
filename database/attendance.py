import sqlite3
from typing import List, Optional, Dict, Any

from .connection import get_connection


def add_attendance(date: str, service_type: str, count: int, note: Optional[str] = None, conn: sqlite3.Connection | None = None) -> int:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute(
            "INSERT INTO attendance (date, service_type, count, note) VALUES (?, ?, ?, ?)",
            (date, service_type, count, note),
        )
        if close:
            conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not add attendance record: {e}")
    finally:
        if close:
            conn.close()


def delete_attendance_by_id(record_id: int, conn: sqlite3.Connection | None = None) -> None:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        conn.execute("DELETE FROM attendance WHERE id = ?", (record_id,))
        if close:
            conn.commit()
    finally:
        if close:
            conn.close()


def delete_attendance(date: str, service_type: str, conn: sqlite3.Connection | None = None) -> None:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        conn.execute("DELETE FROM attendance WHERE date = ? AND service_type = ?", (date, service_type))
        if close:
            conn.commit()
    finally:
        if close:
            conn.close()


def update_attendance(record_id: int, *, date: Optional[str] = None, service_type: Optional[str] = None, count: Optional[int] = None, note: Optional[str] = None, conn: sqlite3.Connection | None = None) -> None:
    fields: List[str] = []
    params: List[Any] = []
    if date is not None:
        fields.append("date = ?")
        params.append(date)
    if service_type is not None:
        fields.append("service_type = ?")
        params.append(service_type)
    if count is not None:
        fields.append("count = ?")
        params.append(count)
    if note is not None:
        fields.append("note = ?")
        params.append(note)

    if not fields:
        return

    params.append(record_id)
    sql = f"UPDATE attendance SET {', '.join(fields)} WHERE id = ?"

    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        conn.execute(sql, tuple(params))
        if close:
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Could not update attendance record: {e}")
    finally:
        if close:
            conn.close()


def get_attendance_by_id(record_id: int, conn: sqlite3.Connection | None = None) -> Optional[Dict[str, Any]]:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute("SELECT * FROM attendance WHERE id = ?", (record_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        if close:
            conn.close()


def get_all_attendance(conn: sqlite3.Connection | None = None) -> List[Dict[str, Any]]:
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        cur = conn.execute("SELECT * FROM attendance ORDER BY date DESC, service_type")
        return [dict(r) for r in cur.fetchall()]
    finally:
        if close:
            conn.close()


def find_attendance(date: Optional[str] = None, service_type: Optional[str] = None, conn: sqlite3.Connection | None = None) -> List[Dict[str, Any]]:
    clauses: List[str] = []
    params: List[Any] = []
    if date is not None:
        clauses.append("date = ?")
        params.append(date)
    if service_type is not None:
        clauses.append("service_type = ?")
        params.append(service_type)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT * FROM attendance {where} ORDER BY date DESC, service_type"

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
    "add_attendance",
    "delete_attendance",
    "delete_attendance_by_id",
    "update_attendance",
    "get_attendance_by_id",
    "get_all_attendance",
    "find_attendance",
]
