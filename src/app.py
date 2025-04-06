# -*- coding: utf-8 -*-
import sys
import time
import sqlite3

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pathlib import Path

sys.argv.append("noprint")
path1 = "i:/core/bots/ma"

path2 = Path(__file__).parent.parent / "bots"  # $HOME/www/python/bots

if Path(path1).exists():
    sys.path.append(path1)
else:
    sys.path.append(str(path2))

try:
    from make2 import event
except:
    event = None

app = Flask(__name__)
CORS(app)  # ← لتفعيل CORS


def init_db():
    conn = sqlite3.connect("api_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            request_data TEXT,
            response_status TEXT NOT NULL,
            response_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_request(endpoint, request_data, response_status, response_time):
    response_time = round(response_time, 3)
    conn = sqlite3.connect("api_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (endpoint, request_data, response_status, response_time)
        VALUES (?, ?, ?, ?)
    """, (endpoint, str(request_data), response_status, response_time))
    conn.commit()
    conn.close()


@app.route("/api/<title>", methods=["GET"])
def get_title(title) -> str:
    # ---
    start_time = time.time()
    # ---
    if event is None:
        log_request("/api/<title>", {"title": title}, "error", time.time() - start_time)
        return jsonify({"error": "حدث خطأ أثناء تحميل المكتبة"})
    # ---
    json_result = event([title], tst_prnt_all=False) or {"result": ""}
    # ---
    data = {}
    # ---
    for x, v in json_result.items():
        data = {"result": v}
        break
    # ---
    delta = time.time() - start_time
    # ---
    # تحديد حالة الاستجابة
    response_status = "success" if data.get("result") else "no_result"
    log_request("/api/<title>", {"title": title}, response_status, delta)
    # ---
    # data["time"] = delta
    # ---
    return jsonify(data)


@app.route("/api/list", methods=["POST"])
def get_titles():
    start_time = time.time()
    data = request.get_json()
    titles = data.get("titles", [])

    # تأكد أن البيانات قائمة
    if not isinstance(titles, list):
        log_request("/api/list", data, "error", time.time() - start_time)
        return jsonify({"error": "بيانات غير صالحة"}), 400

    # print("get_titles:")
    # print(titles)

    if event is None:
        log_request("/api/list", data, "error", time.time() - start_time)
        return jsonify({"error": "حدث خطأ أثناء تحميل المكتبة"})
    # ---
    start_time = time.time()
    # ---
    json_result, no_labs = event(titles, return_no_labs=True, tst_prnt_all=False) or {}
    # ---
    len_result = len(json_result)
    # ---
    for x in no_labs:
        if x not in json_result.keys():
            json_result[x] = ""
    # ---
    delta = time.time() - start_time
    # ---
    response_data = {
        "results" : json_result,
        "no_labs": len(no_labs),
        "with_labs": len_result,
        "time": delta
    }
    # ---
    # تحديد حالة الاستجابة
    response_status = "success" if len_result > 0 else "no_result"
    log_request("/api/list", data, response_status, delta)
    # ---
    return jsonify(response_data)


@app.route("/logs", methods=["GET"])
def view_logs():
    conn = sqlite3.connect("api_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()

    # تحويل السجلات إلى قائمة قابلة للقراءة
    log_list = []
    for log in logs:
        log_list.append({
            "id": log[0],
            "endpoint": log[1],
            "request_data": log[2],
            "response_status": log[3],
            "response_time": log[4],
            "timestamp": log[5]
        })

    return render_template("logs.html", logs=log_list)


@app.route("/", methods=["GET"])
def main() -> str:
    return render_template("index.html")


@app.route("/list", methods=["GET"])
def titles() -> str:
    return render_template("list.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", tt="invalid_url", error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", tt="unexpected_error", error=str(e)), 500


if __name__ == "__main__":
    init_db()  # تهيئة قاعدة البيانات عند بدء التشغيل
    app.run(debug=True)
