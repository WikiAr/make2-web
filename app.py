import sys

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pathlib import Path

path1 = "i:/core/bots/ma"
path2 = Path(__file__).parent

if Path(path1).exists():
    sys.path.append(path1)
else:
    sys.path.append(str(path2))

from make2 import event

app = Flask(__name__)
CORS(app)  # ← لتفعيل CORS


@app.route("/api/<title>", methods=["GET"])
def get_title(title) -> str:
    # ---
    json_result = event([title], tst_prnt_all=False) or {"result": ""}
    # ---
    for x, v in json_result.items():
        return jsonify({"result": v})
    # ---
    return jsonify(json_result)


@app.route("/api/list", methods=["POST"])
def get_titles():
    data = request.get_json()
    titles = data.get("titles", [])

    # تأكد أن البيانات قائمة
    if not isinstance(titles, list):
        return jsonify({"error": "بيانات غير صالحة"}), 400

    # print("get_titles:")
    # print(titles)

    json_result = event(titles, tst_prnt_all=False) or {}
    return jsonify(json_result)


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
