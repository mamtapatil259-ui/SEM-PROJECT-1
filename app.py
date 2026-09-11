from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import pandas as pd

from utils.data_processing import load_dataset, dataset_summary
from utils.analytics import generate_kpis

app = Flask(__name__)
app.secret_key = "dev-secret"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD, exist_ok=True)

ALLOWED = {"csv", "tsv", "txt", "xlsx", "xls", "json", "jsonl"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def current_df():
    path = session.get("dataset_path")
    if not path or not os.path.exists(path):
        raise ValueError("Please upload a dataset first.")
    return load_dataset(path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("dataset_path"):
        return render_template("index.html")
    return render_template("dashboard.html")

@app.post("/api/upload")
def upload():
    try:
        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "Please select a dataset."}), 400
        if not allowed(file.filename):
            return jsonify({"error": "Unsupported file format."}), 400

        token = uuid.uuid4().hex[:8]
        filename = f"{token}_{file.filename}"
        path = os.path.join(UPLOAD, filename)
        file.save(path)

        df = load_dataset(path)
        session["dataset_path"] = path
        session["filename"] = file.filename

        return jsonify({
            "ok": True,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.post("/api/sample")
def sample():
    try:
        csv_text = request.json.get("data", "")
        if not csv_text.strip():
            return jsonify({"error": "No CSV data provided."}), 400

        token = uuid.uuid4().hex[:8]
        path = os.path.join(UPLOAD, f"sample_{token}.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(csv_text)

        df = load_dataset(path)
        session["dataset_path"] = path
        session["filename"] = "sample_data.csv"

        return jsonify({"ok": True, "filename": "sample_data.csv",
                        "rows": len(df), "columns": len(df.columns)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.get("/api/summary")
def summary():
    try:
        return jsonify(dataset_summary(current_df()))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.get("/api/kpis")
def kpis():
    try:
        return jsonify(generate_kpis(current_df()))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
