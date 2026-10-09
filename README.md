# Auto DataDash - Analytics & Dashboard Studio

A full-stack Business Intelligence dashboard application built with a **Frontend designed in HTML & CSS** and a **Backend implemented in Python**.

---

## 🏗 Architecture Overview

```
.
├── backend/
│   ├── server.py        # Python Backend Server (Standard Library - zero pip installs required)
│   ├── flask_app.py     # Python Flask Backend (Alternative for Flask deployments)
│   └── requirements.txt # Python dependencies (optional for Flask/Pandas)
│
├── frontend/
│   ├── index.html       # HTML5 Semantic Interface
│   ├── css/
│   │   └── style.css    # Modern CSS Stylesheet, Animations & Layout
│   └── js/
│       └── app.js       # Client application logic & Chart.js integration
│
├── server.py            # Root Python runner: `python3 server.py`
└── server.ts            # Full-stack Node/Vite bridge for preview & deployment
```

---

## 🚀 How to Run the Application

### Option 1: Run with Pure Python (Recommended)
You only need Python 3 installed. No external packages or pip installs are required.

```bash
# From the project root
python3 server.py
```
Open **`http://localhost:5000`** in your browser.

- Serves the **HTML & CSS frontend** from `frontend/index.html`.
- Serves the **Python Backend REST API** for:
  - `POST /api/analytics/generate-dashboard` (Calculates automated KPIs and visual chart layouts)
  - `POST /api/analytics/clean-suggestions` (Scans missing values and data hygiene)
  - `POST /api/analytics/calculate-kpi` (Calculates SUM, AVERAGE, MIN, MAX aggregations)
  - `POST /api/analytics/query` (Groups and aggregates multi-dimensional records)

---

### Option 2: Run with Python Flask
If you prefer running with Flask:

```bash
cd backend
pip install -r requirements.txt
python flask_app.py
```
Open **`http://localhost:5000`** in your browser.

---

### Option 3: Run the Full-Stack Dev Server (Node + Python Bridge)
```bash
npm run dev
```
Open **`http://localhost:3000`** (or access `/html-view` for the pure HTML/CSS view).

---

## 🎨 Frontend Features (HTML & CSS)
- **Spreadsheet Ingestion**: Drag & drop Excel (`.xlsx`, `.xls`), CSV, and JSON files.
- **Raw Data Table**: Interactive table with live search filtering and CSV export.
- **KPI Scorecards**: Metric scorecards with kinetic count-up animations and live formula aggregations.
- **Graphical Visualizations**: Interactive Bar, Line, Area, Pie, and Donut charts powered by Chart.js.
- **Custom Modals**: Create custom KPIs and design custom charts with column and aggregation pickers.
