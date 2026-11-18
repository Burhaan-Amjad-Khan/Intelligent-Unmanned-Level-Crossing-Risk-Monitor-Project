# Intelligent Unmanned Level-Crossing Risk Monitor
**Project ID:** ISET_IP - 028

> **Safety notice:** This is an educational computer-vision prototype, not certified railway safety equipment. It must never operate barriers/signals or be relied on for train operations or accident prevention.

## Features
- Real webcam/uploaded-video inference with genuine pretrained **Ultralytics YOLO** (`yolo11n.pt`), restricted to person, bicycle, car, motorcycle, bus, truck, and train.
- Normalized configurable danger-zone polygon; bounding-box centroid membership, lightweight IOU tracking, and zone dwell time.
- Transparent rule engine: **SAFE** (clear), **CAUTION** (zone occupied or approach warning), **HIGH RISK** (occupied + approach active). Scores prioritize dashboard attention; they are not accident probabilities.
- Provenance separation: `REAL_YOLO`, `MANUAL INPUT`, and `SIMULATION` are displayed/stored separately. There is no fabricated train/signal data.
- SQLite history, Plotly analytics, warning cooldown/mute/test controls, and six deterministic simulations.

## Windows setup
1. Install **Python 3.11 (64-bit)** from https://www.python.org/downloads/windows/ and select **Add Python to PATH**. Restart VS Code.
2. Open PowerShell in this directory:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Select **Live Monitor**, choose Webcam (index 0) or upload a video, then **Start**. The first real inference downloads `yolo11n.pt`; use internet or pre-cache the Ultralytics model.
4. Select a scenario in the sidebar and **Run selected simulation** to demonstrate all states without hardware.

## Testing
```powershell
pytest -q
```

## Data and operating notes
- Database: `data/crossing_monitor.db`, initialized automatically.
- Webcam, model download, graphics/audio devices and uploaded footage require local execution; failures are surfaced in the UI rather than replaced with invented results.
- For a real train-approach system, integrate only an approved, independently validated input interface. This code currently supports manual input or labeled simulation only.

## Report / demonstration
Run `python tools/generate_report.py` after dependencies are installed to create `reports/project_report.pdf`. `demo/DEMONSTRATION_SCRIPT.md` is a truthful 3–5 minute recording script; create the MP4 from your locally running dashboard after capturing genuine screens. The repository deliberately does not include a fabricated “actual demo” MP4.
