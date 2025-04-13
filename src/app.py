# -*- coding: utf-8 -*-
import os
import sys
import time
from flask import Flask, jsonify, render_template, request
# from flask_cors import CORS

import logs_db

sys.argv.append("noprint")

path1 = "i:/core/bots/ma"

HOME = os.getenv("HOME")

if HOME:
    path2 = HOME + "/www/python/bots"
    sys.path.append(str(path2))
else:
    sys.path.append(path1)
# ---
try:
    from make2 import event
except:
    event = None

app = Flask(__name__)
# CORS(app)  # ← لتفعيل CORS


@app.route("/api/<title>", methods=["GET"])
def get_title(title) -> str:
    # Check for User-Agent header
    if not request.headers.get('User-Agent'):
        return jsonify({"error": "User-Agent header is required"}), 400
    # ---
    start_time = time.time()
    # ---
    if event is None:
        logs_db.log_request("/api/<title>", title, "error", time.time() - start_time)
        return jsonify({"error": "حدث خطأ أثناء تحميل المكتبة"})
    # ---
    json_result = event([title], tst_prnt_all=False) or {"result": ""}
    # ---
    data = {}
    # ---
    # for x, v in json_result.items(): data = {"result": v} break
    # ---
    data = {"result": next(iter(json_result.values()), "")}
    # ---
    delta = time.time() - start_time
    # ---
    # تحديد حالة الاستجابة
    response_status = data.get("result") if data.get("result") else "no_result"
    logs_db.log_request("/api/<title>", title, response_status, delta)
    # ---
    # data["time"] = delta
    # ---
    return jsonify(data)


@app.route("/api/list", methods=["POST"])
def get_titles():
    # Check for User-Agent header
    if not request.headers.get('User-Agent'):
        return jsonify({"error": "User-Agent header is required"}), 400
    # ---
    start_time = time.time()
    data = request.get_json()
    titles = data.get("titles", [])
    # ---
    len_titles = len(titles)
    titles = list(set(titles))
    duplicates = len_titles - len(titles)
    # ---
    # تأكد أن البيانات قائمة
    if not isinstance(titles, list):
        logs_db.log_request("/api/list", titles, "error", time.time() - start_time)
        return jsonify({"error": "بيانات غير صالحة"}), 400

    # print("get_titles:")
    # print(titles)

    if event is None:
        logs_db.log_request("/api/list", titles, "error", time.time() - start_time)
        return jsonify({"error": "حدث خطأ أثناء تحميل المكتبة"})
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
        "duplicates": duplicates,
        "time": delta
    }
    # ---
    # تحديد حالة الاستجابة
    response_status = "success" if len_result > 0 else "no_result"
    logs_db.log_request("/api/list", titles, response_status, delta)
    # ---
    return jsonify(response_data)


@app.route("/logs", methods=["GET"])
def view_logs():
    # ---
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order = request.args.get('order', 'asc').upper()
    order_by = request.args.get('order_by', 'timestamp')

    # Validate values
    page = max(1, page)
    per_page = max(1, min(100, per_page))

    # Offset for pagination
    offset = (page - 1) * per_page
    # ---
    order_by_types = [
        "id",
        "endpoint",
        "request_data",
        "response_status",
        "response_time",
        "response_count",
        "timestamp",
    ]
    # ---
    if order_by not in order_by_types:
        order_by = "timestamp"
    # ---
    logs = logs_db.get_logs(per_page, offset, order, order_by=order_by)
    # ---
    total_logs = logs_db.count_all()
    # ---
    # Convert to list of dicts
    log_list = []
    for log in logs:
        # {'id': 1, 'endpoint': 'api', 'request_data': 'Category:1934-35 in Bulgarian football', 'response_status': 'true', 'response_time': 123123.0, 'response_count': 6, 'timestamp': '2025-04-10 01:08:58'}
        # ---
        log_list.append({
            "id": log["id"],
            "endpoint": log["endpoint"],
            "request_data": log["request_data"],
            "response_status": log["response_status"],
            "response_time": log["response_time"],
            "timestamp": log["timestamp"],
            "response_count": log["response_count"],
        })
    # ---
    # Pagination calculations
    total_pages = (total_logs + per_page - 1) // per_page
    start_log = (page - 1) * per_page + 1
    end_log = min(page * per_page, total_logs)
    start_page = max(1, page - 2)
    end_page = min(start_page + 4, total_pages)
    start_page = max(1, end_page - 4)
    # ---
    return render_template(
        "logs.html",
        logs=log_list,
        order_by_types=order_by_types,
        page=page,
        order_by=order_by,
        per_page=per_page,
        total_pages=total_pages,
        total_logs=total_logs,
        start_log=start_log,
        end_log=end_log,
        start_page=start_page,
        end_page=end_page,
        order=order
    )


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
    logs_db.init_db()
    # ---
    debug = "debug" in sys.argv
    # ---
    app.run(debug=debug)
