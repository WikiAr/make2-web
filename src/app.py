# -*- coding: utf-8 -*-
import sys
import time

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


@app.route("/api/<title>", methods=["GET"])
def get_title(title) -> str:
    # ---
    # start_time = time.time()
    # ---
    if event is None:
        return jsonify({"error": "حدث خطأ أثناء تحميل المكتبة"})
    # ---
    json_result = event([title], tst_prnt_all=False) or {"result": ""}
    # ---
    # delta = time.time() - start_time
    # ---
    data = {}
    # ---
    for x, v in json_result.items():
        data = {"result": v}
        break
    # ---
    # data["time"] = delta
    # ---
    return jsonify(data)


@app.route("/api/list", methods=["POST"])
def get_titles():
    data = request.get_json()
    titles = data.get("titles", [])

    # تأكد أن البيانات قائمة
    if not isinstance(titles, list):
        return jsonify({"error": "بيانات غير صالحة"}), 400

    # print("get_titles:")
    # print(titles)

    if event is None:
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
    data = {
        "results" : json_result,
        "no_labs": len(no_labs),
        "with_labs": len_result,
        "time": delta
    }
    # ---
    return jsonify(data)


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
    app.run(debug=True)
