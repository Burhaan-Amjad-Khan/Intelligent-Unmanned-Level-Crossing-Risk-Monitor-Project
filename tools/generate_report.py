"""Generate an honest project report; add only screenshots captured from a local real run."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/"reports"/"project_report.pdf"; out.parent.mkdir(exist_ok=True)
styles=getSampleStyleSheet(); story=[]
def section(title, body):
    story.extend([Paragraph(title,styles["Heading1"]),Paragraph(body,styles["BodyText"]),Spacer(1,10)])
story += [Paragraph("Intelligent Unmanned Level-Crossing Risk Monitor",styles["Title"]),Paragraph("Project ID: ISET_IP - 028",styles["Heading2"]),Spacer(1,30),Paragraph("Educational Prototype Report",styles["Heading2"]),Spacer(1,30),Paragraph("Safety notice: This prototype is not a certified railway safety system and must not control railway infrastructure.",styles["BodyText"]),PageBreak()]
section("Abstract", "A Python dashboard prototype monitors a webcam or uploaded video with genuine pretrained Ultralytics YOLO inference. It overlays a configurable track danger zone, applies a transparent rule-based risk assessment, records provenance-aware history in SQLite, and exposes repeatable labeled simulations.")
section("Problem statement and objectives", "Unmanned crossings can have vulnerable road users or vehicles near tracks. The objective is to demonstrate visual situational awareness—not automated operational control—by identifying supported visible object classes and prioritizing attention.")
section("Existing and proposed system", "The proposed dashboard combines video input, YOLO, centroid-zone geometry, lightweight IOU association, a rule engine, SQLite storage, alert controls and Plotly analytics. It has no integration to barrier, signal or train-control systems.")
section("Architecture and workflow", "Video frame → YOLO detection → supported-class filter → IOU tracker → polygon centroid test and dwell time → risk calculator → display / optional local alert / SQLite event history → analytics. Train approach is either explicitly MANUAL INPUT or explicitly SIMULATED TRAIN APPROACH.")
section("Hardware, software and technologies", "Windows 10/11, Python 3.11, a webcam or video file for live operation, Python, Streamlit, OpenCV, Ultralytics, NumPy, SQLite, Plotly, Pygame and Pytest. First YOLO inference may require internet to retrieve yolo11n.pt.")
section("Methodology", "YOLO detections are genuine model outputs only. The zone polygon uses normalized coordinates and OpenCV point-in-polygon testing of each object centroid. The tracker associates same-label boxes by intersection-over-union. This is a prototype and not robust multi-camera safety tracking.")
section("Risk algorithm", "SAFE (score 0): clear zone and no approach warning. CAUTION (score 30): approach warning with clear zone; CAUTION (score 50+, increasing for occupancy/dwell): object in zone. HIGH RISK (score 85+): approach active and object in zone. Scores are prioritization values, not accident probabilities.")
section("Alerts, database and dashboard", "The interface uses green/yellow/red states, mute and audible-test controls. Alert playback failures are reported safely. SQLite records timestamp, input mode, object details, zone state, duration, risk, approach source/status and description. Simulations are stored as SIMULATION, never REAL VIDEO.")
section("Simulation scenarios", "The dashboard includes empty crossing (SAFE); vehicle, pedestrian, and sustained obstacle occupancy (CAUTION); approach plus occupied zone (HIGH RISK); and zone clears (SAFE). Each is labeled simulation.")
section("Test cases and actual results", "Automated tests are supplied in tests/. At report-generation time this document does not claim pass results; run pytest -q on the target machine and attach its real output. Hardware and model inference require local runtime validation with a real source and model weight.")
section("Screenshots", "Capture only authentic local dashboard/screens and insert them in a future evidence revision. No screenshots are fabricated by this generator.")
section("Advantages, limitations and future scope", "Advantages include transparent logic, local storage and clear input provenance. Limitations include model sensitivity, visibility/weather constraints, lightweight tracking, no sensor fusion and no certified train feed. Future work requires approved data interfaces, rigorous dataset evaluation, redundancy, cybersecurity and independent railway safety certification.")
section("Conclusion and references", "This project is a demonstration platform for AI-assisted visual awareness, not operational protection. References: Ultralytics documentation (https://docs.ultralytics.com/); OpenCV documentation (https://docs.opencv.org/); Streamlit documentation (https://docs.streamlit.io/).")
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm).build(story)
print(out)
