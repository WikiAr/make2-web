# -*- coding: utf-8 -*-
import os
# import sys
# import json
import sqlite3
from pathlib import Path

HOME = os.getenv("HOME")

main_path = Path(__file__).parent.parent.parent
# ---
if HOME:
    main_path = HOME + "/www/python/dbs"
# ---
db_path = f"{str(main_path)}/new_logs.db"

db_path_main = {1: str(db_path)}

print("db_path", db_path_main[1])


def change_db_path(file):
    # ---
    db_path = str(main_path) + f"/{file}"
    # ---
    dbs_path = Path(main_path)
    # ---
    # list of files *.db in dbs_path
    dbs = [str(f.name) for f in dbs_path.glob("*.db") if f.is_file()]
    # ---
    if file in dbs and os.path.exists(db_path):
        db_path_main[1] = str(db_path)
    # ---
    return dbs


def db_commit(query, params=[]):
    try:
        with sqlite3.connect(db_path_main[1]) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"init_db Database error: {e}")
        return e


def init_db():
    # ---
    query_x = """
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT NOT NULL,
        request_data TEXT,
        response_status TEXT NOT NULL,
        response_time REAL,
        response_count INTEGER DEFAULT 1,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )"""
    # ---
    query = """
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT NOT NULL,
        request_data TEXT NOT NULL,
        response_status TEXT NOT NULL,
        response_time REAL,
        response_count INTEGER DEFAULT 1,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(request_data, response_status)
    );"""
    # ---
    db_commit(query)
    # ---
    query = """
    CREATE TABLE IF NOT EXISTS list_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT NOT NULL,
        request_data TEXT NOT NULL,
        response_status TEXT NOT NULL,
        response_time REAL,
        response_count INTEGER DEFAULT 1,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(request_data, response_status)
    );"""
    # ---
    db_commit(query)


def fetch_all(query, params=[], fetch_one=False):
    try:
        with sqlite3.connect(db_path_main[1]) as conn:
            # Set row factory to return rows as dictionaries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(query, params)

            # Fetch results
            if fetch_one:
                row = cursor.fetchone()
                logs = dict(row) if row else None  # Convert to dictionary
            else:
                rows = cursor.fetchall()
                logs = [dict(row) for row in rows]  # Convert all rows to dictionaries

    except sqlite3.Error as e:
        print(f"Database error in view_logs: {e}")
        if "no such table" in str(e):
            init_db()
        logs = []

    return logs


def log_request(endpoint, request_data, response_status, response_time):
    # ---
    response_time = round(response_time, 3)
    # ---
    response_status = str(response_status)
    # ---
    table_name = "logs" if endpoint != "/api/list" else "list_logs"
    # ---
    result = db_commit(
        f"""
        INSERT INTO {table_name} (endpoint, request_data, response_status, response_time)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(request_data, response_status) DO UPDATE SET
            response_count = response_count + 1,
            response_time = excluded.response_time,
            timestamp = CURRENT_TIMESTAMP
    """,
        (endpoint, str(request_data), response_status, response_time),
    )
    # ---
    if result is not True:
        print(f"Error logging request: {result}")
        if "no such table" in str(result):
            init_db()
    # ---
    return result


def add_status(query, params, status="", like=""):
    # ---
    if not isinstance(params, list):
        params = list(params)
    # ---
    if status:
        if status == "Category":
            query += " WHERE response_status like 'تصنيف%'"
        else:
            query += " WHERE response_status = ?"
            params.append(status)
    elif like:
        query += " WHERE response_status like ?"
        params.append(like)
    # ---
    # params = tuple(params)
    # ---
    return query, params


def sum_response_count(status="", table_name="logs", like=""):
    # ---
    query = f"select sum(response_count) as count_all from {table_name}"
    # ---
    params = []
    # ---
    query, params = add_status(query, params, status=status, like=like)
    # ---
    result = fetch_all(query, params, fetch_one=True)
    # ---
    print("result", result)
    # ---
    result = result["count_all"] or 0
    # ---
    return result


def get_response_status(table_name="logs"):
    # ---
    query = f"select response_status, count(response_status) as numbers from {table_name} group by response_status having count(*) > 2"
    # ---
    result = fetch_all(query, ())
    # ---
    result = [row['response_status'] for row in result]
    # ---
    return result


def count_all(status="", table_name="logs", like=""):
    # ---
    query = f"SELECT COUNT(*) FROM {table_name}"
    # ---
    params = []
    # ---
    query, params = add_status(query, params, status=status, like=like)
    # ---
    result = fetch_all(query, params, fetch_one=True)
    # ---
    if not result:
        return 0
    # ---
    if isinstance(result, list):
        result = result[0]
    # ---
    total_logs = result["COUNT(*)"]
    # ---
    return total_logs


def get_logs(per_page=10, offset=0, order="DESC", order_by="timestamp", status="", table_name="logs", like=""):
    # ---
    if order not in ["ASC", "DESC"]:
        order = "DESC"
    # ---
    query = f"SELECT * FROM {table_name} "
    # ---
    params = []
    # ---
    query, params = add_status(query, params, status=status, like=like)
    # ---
    query += f"ORDER BY {order_by} {order} LIMIT ? OFFSET ?"
    # ---
    # {'id': 1, 'endpoint': 'api', 'request_data': 'Category:1934-35 in Bulgarian football', 'response_status': 'true', 'response_time': 123123.0, 'response_count': 6, 'timestamp': '2025-04-10 01:08:58'}
    # ---
    params.extend([per_page, offset])
    # ---
    logs = fetch_all(query, params)
    # ---
    return logs


if __name__ == "__main__":
    # python3 I:/core/bots/ma/web/src/logs_db/bot.py
    init_db()
    # ---
    print("count_all", count_all(status="no_result"))
    # ---
    print("get_response_status", get_response_status())
    # ---
    # print("get_logs", get_logs(status=""))
    print("get_logs", get_logs(status="no_result"))
