from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "questions.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify(load_data())

@app.route("/api/questions", methods=["POST"])
def add_question():
    data = load_data()
    q = request.json
    q["id"] = int(datetime.now().timestamp() * 1000)
    q["marked"] = False
    data.append(q)
    save_data(data)
    return jsonify(q), 201

@app.route("/api/questions/<int:qid>", methods=["PUT"])
def update_question(qid):
    data = load_data()
    for i, q in enumerate(data):
        if q["id"] == qid:
            updated = request.json
            updated["id"] = qid
            data[i] = updated
            save_data(data)
            return jsonify(updated)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/questions/<int:qid>", methods=["DELETE"])
def delete_question(qid):
    data = load_data()
    data = [q for q in data if q["id"] != qid]
    save_data(data)
    return jsonify({"ok": True})

@app.route("/api/questions/<int:qid>/bookmark", methods=["POST"])
def toggle_bookmark(qid):
    data = load_data()
    for q in data:
        if q["id"] == qid:
            q["marked"] = not q.get("marked", False)
            save_data(data)
            return jsonify(q)
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    print("\n✅  Interview Question Bank is running!")
    print("👉  Open your browser and go to:  http://127.0.0.1:5000\n")
    app.run(debug=True)
