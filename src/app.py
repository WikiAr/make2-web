# -*- coding: utf-8 -*-
import os
import sys
import time
from flask import Flask, render_template, request, Response
import json
# from flask_cors import CORS

import logs_db
import logs_bot

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
except ImportError:
    event = None

app = Flask(__name__)
# CORS(app)  # ← لتفعيل CORS

def jsonify(data : dict) -> str:
    response_json = json.dumps(data, ensure_ascii=False, indent=4)
    return Response(response=response_json, content_type="application/json; charset=utf-8")

@app.route("/api/logs_by_day", methods=["GET"])
def get_logs_by_day() -> str:
    result = logs_bot.logs_by_day(request)
    return jsonify(result)

@app.route("/api/<title>", methods=["GET"])
def get_title(title) -> str:
    # ---
    start_time = time.time()
    # ---
    # Check for User-Agent header
    if not request.headers.get("User-Agent"):
        response_status = "User-Agent missing"
        logs_db.log_request("/api/<title>", title, response_status, time.time() - start_time)
        return jsonify({"error": "User-Agent header is required"}), 400
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
    # ---
    data['sql'] = logs_db.log_request("/api/<title>", title, response_status, delta)
    # ---
    # data["time"] = delta
    # ---
    return jsonify(data)


@app.route("/api/list", methods=["POST"])
def get_titles():
    # ---
    start_time = time.time()
    data = request.get_json()
    titles = data.get("titles", [])
    # ---
    delta = time.time() - start_time
    # ---
    len_titles = len(titles)
    titles = list(set(titles))
    duplicates = len_titles - len(titles)
    # ---
    # Check for User-Agent header
    if not request.headers.get("User-Agent"):
        response_status = "User-Agent missing"
        logs_db.log_request("/api/list", titles, response_status, delta)
        return jsonify({"error": "User-Agent header is required"}), 400
    # ---
    # تأكد أن البيانات قائمة
    if not isinstance(titles, list):
        logs_db.log_request("/api/list", titles, "error", delta)
        return jsonify({"error": "بيانات غير صالحة"}), 400

    # print("get_titles:")
    # print(titles)

    if event is None:
        logs_db.log_request("/api/list", titles, "error", delta)
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
    delta2 = time.time() - start_time
    # ---
    response_data = {"results": json_result, "no_labs": len(no_labs), "with_labs": len_result, "duplicates": duplicates, "time": delta2}
    # ---
    # تحديد حالة الاستجابة
    response_status = "success" if len_result > 0 else "no_result"
    logs_db.log_request("/api/list", titles, response_status, delta2)
    # ---
    return jsonify(response_data)


@app.route("/logs1", methods=["GET"])
def view_logs():
    # ---
    result = logs_bot.view_logs(request)
    # ---
    return render_template("logs.html", logs=result["logs"], order_by_types=result["order_by_types"], tab=result["tab"], status_table=result["status_table"], dbs=result["dbs"])

@app.route("/logs_by_day", methods=["GET"])
def logs_by_day():
    # ---
    result = logs_bot.logs_by_day(request)
    # ---
    return render_template("logs_by_day.html", logs=result["logs"], order_by_types=result["order_by_types"], tab=result["tab"], status_table=result["status_table"], dbs=result["dbs"])


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
