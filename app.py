from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import json
import os

LOCK = threading.Lock()
SCORES_FILE = "scores.json"

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_scores(data):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/api/scores", methods=["GET"])
def get_scores():
    with LOCK:
        data = load_scores()
    # retornar lista ordenada por score desc
    items = [{"name": k, "score": v} for k, v in data.items()]
    items.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(items), 200

@app.route("/api/score", methods=["POST"])
def post_score():
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error": "JSON body required"}), 400

    name = payload.get("name", "")
    score = payload.get("score")

    if not isinstance(name, str) or len(name.strip()) == 0:
        return jsonify({"error": "Nome inválido"}), 400

    name = name.strip()[:5]  # garantir no backend também (máx 5 chars)
    if len(name) > 5:
        return jsonify({"error": "Nome deve ter no máximo 5 caracteres"}), 400

    if not (isinstance(score, int) and score >= 0):
        return jsonify({"error": "Score inválido"}), 400

    with LOCK:
        data = load_scores()
        prev = data.get(name, 0)
        if score > prev:
            data[name] = score
            save_scores(data)

    return jsonify({"ok": True, "name": name, "score": score}), 201

# Serve arquivos estáticos (index.html, css, js, etc.)
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_file(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    # cria arquivo inicial se não existir
    if not os.path.exists(SCORES_FILE):
        save_scores({})
    app.run(host="0.0.0.0", port=5000, debug=False)

