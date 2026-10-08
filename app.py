from flask import Flask, render_template, request, jsonify, session, send_file
import os
import sqlite3
import json
import io
import uuid
import numpy as np
import pandas as pd

from werkzeug.utils import secure_filename

from utils.data_processing import load_dataset, clean_dataset, dataset_summary, column_profile
from utils.analytics import generate_kpis, generate_insights
from utils.visualization import create_chart
from utils.ml_model import dataset_ml_summary

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD = os.path.join(BASE, "uploads")
DB = os.path.join(BASE, "database", "dashboard.db")
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(os.path.dirname(DB), exist_ok=True)

# Supported analytical formats.
ALLOWED = {"csv", "tsv", "txt", "xlsx", "xls", "json", "jsonl", "parquet", "xml"}


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


def current_df():
    path = session.get("working_path") or session.get("dataset_path")
    if not path or not os.path.exists(path):
        raise ValueError("Please upload a dataset first.")
    return load_dataset(path)


def dataframe_path(df):
    """Persist the live edited dataframe in a lossless internal CSV snapshot."""
    path = session.get("working_path")
    if not path:
        token = uuid.uuid4().hex[:10]
        path = os.path.join(UPLOAD, f"working_{token}.csv")
        session["working_path"] = path
    df.to_csv(path, index=False)
    return path


def save_original_format(df, extension):
    """Create a downloadable copy in the requested format."""
    ext = extension.lower().lstrip(".")
    bio = io.BytesIO()
    if ext == "csv":
        bio.write(df.to_csv(index=False).encode("utf-8"))
    elif ext == "tsv":
        bio.write(df.to_csv(index=False, sep="\t").encode("utf-8"))
    elif ext == "json":
        bio.write(df.to_json(orient="records", indent=2, force_ascii=False).encode("utf-8"))
    elif ext == "jsonl":
        bio.write(df.to_json(orient="records", lines=True, force_ascii=False).encode("utf-8"))
    elif ext in {"xlsx", "xls"}:
        with pd.ExcelWriter(bio, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
    elif ext == "parquet":
        df.to_parquet(bio, index=False)
    elif ext == "xml":
        bio.write(df.to_xml(index=False).encode("utf-8"))
    elif ext == "txt":
        bio.write(df.to_csv(index=False, sep="\t").encode("utf-8"))
    else:
        raise ValueError("Unsupported export format.")
    bio.seek(0)
    return bio


def persist_df(df):
    """Save the live dataframe and mirror it to SQLite for the project demo."""
    dataframe_path(df)
    with sqlite3.connect(DB) as con:
        df.to_sql("dataset", con, if_exists="replace", index=False)


def json_rows(df, limit=200):
    clean = df.head(limit).copy()
    clean = clean.replace({np.nan: None})
    return clean.to_dict("records")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.post("/api/upload")
def upload():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify(error="No file selected."), 400
    if not allowed(file.filename):
        return jsonify(error="Supported files: CSV, TSV/TXT, Excel, JSON/JSONL, Parquet and XML."), 400

    original_name = secure_filename(file.filename)
    token = uuid.uuid4().hex[:8]
    filename = f"{token}_{original_name}"
    path = os.path.join(UPLOAD, filename)

    try:
        file.save(path)
        df = load_dataset(path)
        if df.empty:
            raise ValueError("The uploaded dataset is empty.")
        session["dataset_path"] = path
        session["dataset_name"] = original_name
        session["working_path"] = None
        persist_df(df)
        return jsonify(
            success=True,
            filename=original_name,
            rows=len(df),
            columns=len(df.columns),
            summary=dataset_summary(df),
            profiles=column_profile(df),
        )
    except Exception as e:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
        return jsonify(error=str(e)), 400


@app.post("/api/sample")
def sample():
    """Load comma-separated sample data pasted by the user."""
    body = request.get_json(silent=True) or {}
    text = body.get("text", "").strip()
    if not text:
        return jsonify(error="Paste CSV data first."), 400
    try:
        df = pd.read_csv(io.StringIO(text))
        if df.empty:
            raise ValueError("Sample data is empty.")
        # Save a local source snapshot.
        name = f"sample_{uuid.uuid4().hex[:8]}.csv"
        path = os.path.join(UPLOAD, name)
        df.to_csv(path, index=False)
        session["dataset_path"] = path
        session["dataset_name"] = name
        session["working_path"] = None
        persist_df(df)
        return jsonify(success=True, filename=name, rows=len(df), columns=len(df.columns), summary=dataset_summary(df))
    except Exception as e:
        return jsonify(error=f"Could not read sample data: {e}"), 400


@app.get("/api/data")
def data():
    try:
        df = current_df()
        return jsonify(
            columns=[str(c) for c in df.columns],
            rows=json_rows(df, 200),
            total_rows=int(len(df)),
            filename=session.get("dataset_name"),
            editable=True,
            preview_limit=200,
        )
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/summary")
def summary():
    try:
        return jsonify(dataset_summary(current_df()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/profile")
def profile():
    try:
        return jsonify(profiles=column_profile(current_df()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/kpis")
def kpis():
    try:
        return jsonify(generate_kpis(current_df()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/insights")
def insights():
    try:
        return jsonify(insights=generate_insights(current_df()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.post("/api/clean")
def clean():
    try:
        body = request.get_json(silent=True) or {}
        df = current_df()
        cleaned_df, report = clean_dataset(
            df,
            remove_duplicates=body.get("remove_duplicates", True),
            trim_strings=body.get("trim_strings", True),
            fill_numeric=body.get("fill_numeric", False),
            drop_null_rows=body.get("drop_null_rows", False),
        )
        persist_df(cleaned_df)
        return jsonify(success=True, filename=session.get("dataset_name"), report=report, summary=dataset_summary(cleaned_df))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.post("/api/cell")
def update_cell():
    """Edit one cell and immediately make every analysis use the new value."""
    try:
        body = request.get_json(silent=True) or {}
        row_index = int(body.get("row_index"))
        column = body.get("column")
        value = body.get("value")
        df = current_df()
        if column not in df.columns:
            raise ValueError("Invalid column.")
        if row_index < 0 or row_index >= len(df):
            raise ValueError("Invalid row index.")

        old = df.iloc[row_index][column]
        series = df[column]
        if pd.api.types.is_numeric_dtype(series):
            if value in (None, ""):
                df.iloc[row_index, df.columns.get_loc(column)] = np.nan
            else:
                number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
                if pd.isna(number):
                    raise ValueError(f"'{value}' is not a valid number for {column}.")
                df.iloc[row_index, df.columns.get_loc(column)] = number
        else:
            df.iloc[row_index, df.columns.get_loc(column)] = "" if value is None else str(value)
        persist_df(df)
        return jsonify(success=True, old_value=None if pd.isna(old) else str(old), summary=dataset_summary(df))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.post("/api/row")
def row_action():
    """Add or delete a row from the live dataset."""
    try:
        body = request.get_json(silent=True) or {}
        action = body.get("action")
        df = current_df()
        if action == "add":
            values = body.get("values") or {}
            row = {c: values.get(c, None) for c in df.columns}
            new = pd.DataFrame([row])
            # Coerce numeric columns where possible.
            for c in df.select_dtypes(include=np.number).columns:
                new[c] = pd.to_numeric(new[c], errors="coerce")
            df = pd.concat([df, new], ignore_index=True)
        elif action == "delete":
            row_index = int(body.get("row_index"))
            if row_index < 0 or row_index >= len(df):
                raise ValueError("Invalid row index.")
            df = df.drop(df.index[row_index]).reset_index(drop=True)
        else:
            raise ValueError("Action must be 'add' or 'delete'.")
        persist_df(df)
        return jsonify(success=True, total_rows=len(df), rows=json_rows(df, 200), summary=dataset_summary(df))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.post("/api/filter")
def filter_data():
    try:
        body = request.get_json(silent=True) or {}
        df = current_df()
        column = body.get("column")
        value = str(body.get("value", ""))
        if column not in df.columns:
            raise ValueError("Invalid column.")
        filtered = df[df[column].astype(str).str.contains(value, case=False, na=False, regex=False)] if value else df
        return jsonify(count=len(filtered), rows=json_rows(filtered, 200))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.post("/api/chart")
def chart():
    try:
        body = request.get_json(silent=True) or {}
        fig = create_chart(current_df(), body.get("chart_type", "bar"), body.get("x"), body.get("y"), body.get("title", "Visualization"))
        return jsonify(json.loads(fig.to_json()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/ml-summary")
def ml_summary():
    try:
        return jsonify(dataset_ml_summary(current_df()))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.get("/api/download/<fmt>")
def download(fmt):
    try:
        df = current_df()
        fmt = fmt.lower()
        if fmt not in ALLOWED:
            raise ValueError("Unsupported export format.")
        bio = save_original_format(df, fmt)
        base = os.path.splitext(session.get("dataset_name", "dataset"))[0]
        filename = f"{base}_edited.{fmt if fmt != 'xls' else 'xlsx'}"
        mimetypes = {
            "csv": "text/csv", "tsv": "text/tab-separated-values", "txt": "text/plain",
            "json": "application/json", "jsonl": "application/json", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "xls": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "parquet": "application/octet-stream", "xml": "application/xml",
        }
        return send_file(bio, as_attachment=True, download_name=filename, mimetype=mimetypes.get(fmt, "application/octet-stream"))
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.errorhandler(413)
def file_too_large(error):
    return jsonify(error="File is too large. Maximum allowed size is 50 MB."), 413


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
