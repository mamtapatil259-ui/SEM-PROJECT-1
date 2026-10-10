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

## ⚡ VS Code & Windows PowerShell Quickstart (1-Click Run)

### 🚀 Copy-Paste Master One-Liner (Inside VS Code Terminal: `Ctrl + ~`):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\run.ps1
```

### ⌨️ Native VS Code Shortcuts:
- **`Ctrl + Shift + B`** (Run Build Task): Automatically runs `run.ps1` in the integrated terminal, auto-checks Python, clears port collisions, launches the backend, and opens the dashboard!
- **`F5`** (Debug): Select **Python: Auto DataDash Server (Port 5000)** to launch with full VS Code breakpoints and step debugging.
- **VS Code Simple Browser**: Press `Ctrl + Shift + P` -> Type `Simple Browser: Show` -> Enter `http://localhost:5000` to view the full HTML/CSS dashboard right inside your VS Code window!

---

## 🪟 Advanced PowerShell Commands & Options

You can pass custom parameters directly into `run.ps1`:

```powershell
# Default launch on port 5000
.\run.ps1

# Custom port (e.g. port 8080 or 5001)
.\run.ps1 -Port 8080

# Launch Flask backend instead of standard library
.\run.ps1 -Mode flask

# Launch Streamlit analytics dashboard (port 8501)
.\run.ps1 -Mode streamlit -Port 8501

# Headless mode (do not automatically open web browser)
.\run.ps1 -NoBrowser

# Force dependency reinstallation
.\run.ps1 -ForceReinstall
```

### 🛠️ What `run.ps1` Does Automatically:
1. **Self-Healing Python Detection**: Checks `python`, `py`, `python3`, detects Microsoft Store stub traps, and searches standard installation folders.
2. **Auto-Install via Winget**: If Python is missing, offers silent automatic installation via `winget install Python.Python.3.11` and updates `$env:PATH` immediately without restarting VS Code.
3. **Port Conflict Killer**: Detects if port 5000 is occupied by a lingering process and safely clears it before binding.
4. **Virtual Environment Isolation**: Creates `.venv`, upgrades pip, and configures `.vscode/settings.json`.
5. **Color-Coded Status Output**: Shows exact endpoints, health checks, and quick links.

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
