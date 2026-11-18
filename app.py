import tempfile
from pathlib import Path
import cv2
import pandas as pd
import streamlit as st
from config.settings import APP_TITLE, PROJECT_ID, DEFAULT_CONFIDENCE, DEFAULT_ZONE, ALERT_COOLDOWN_SECONDS
from detection.detector import YOLODetector
from detection.object_tracker import CentroidTracker
from monitoring.camera import VideoSource
from monitoring.danger_zone import parse_zone
from monitoring.video_processor import VideoProcessor
from risk_engine.risk_calculator import RiskCalculator
from alerts.alarm import Alarm
from alerts.notifications import alert_description
from database.db_manager import DatabaseManager
from dashboard.components import risk_banner, metric_row, analytics
from simulation.scenarios import SCENARIOS, scenario

st.set_page_config(page_title=APP_TITLE, page_icon="🚆", layout="wide")
st.markdown("<style>.stApp{background:#080d18;color:#e5e7eb}.block-container{padding-top:1.3rem}h1,h2,h3{color:#f8fafc}</style>",unsafe_allow_html=True)
@st.cache_resource
def services(): return YOLODetector(), CentroidTracker(), VideoSource(), RiskCalculator(), Alarm(), DatabaseManager()
def init():
    if "last_assessment" not in st.session_state:
        st.session_state.last_assessment=RiskCalculator().assess([])
        st.session_state.running=False; st.session_state.input_mode="NONE"
init(); detector,tracker,camera,calculator,alarm,db=services(); db.initialize()

st.title(f"🚆 {APP_TITLE}")
st.caption(f"{PROJECT_ID} | Educational prototype — not certified railway safety equipment. Never use to control barriers, signals, or train operations.")
page=st.sidebar.radio("OPERATIONS",["Overview","Live Monitor","Risk","Alerts & History","Analytics","Settings"])
st.sidebar.divider(); st.sidebar.caption("DATA INTEGRITY")
st.sidebar.info("Real YOLO detections, manual train input, and simulated scenarios are always labeled separately.")
zone_text=st.sidebar.text_area("Danger-zone polygon (normalized x,y; ...)", "; ".join(f"{x},{y}" for x,y in DEFAULT_ZONE))
try: zone=parse_zone(zone_text)
except ValueError as exc: st.sidebar.error(str(exc)); zone=DEFAULT_ZONE
confidence=st.sidebar.slider("YOLO confidence",.10,.95,DEFAULT_CONFIDENCE,.05)
alarm.muted=st.sidebar.toggle("Mute audio",value=alarm.muted)
sim_name=st.sidebar.selectbox("SIMULATION SCENARIO",list(SCENARIOS))
if st.sidebar.button("Run selected simulation",use_container_width=True):
    objs, train, source=scenario(sim_name); assessment=calculator.assess(objs,train,source)
    st.session_state.last_assessment=assessment; st.session_state.input_mode="SIMULATION"
    st.session_state.sim_objects=objs; st.session_state.sim_train=train; st.session_state.sim_source=source
    desc=alert_description(assessment,"SIMULATED INPUTS")
    db.record(assessment,objs,"SIMULATION",source,train,desc)
    if assessment.state=="HIGH RISK": alarm.beep(assessment.state,ALERT_COOLDOWN_SECONDS)
    st.sidebar.success(f"Simulation applied: {assessment.state}")
assessment=st.session_state.last_assessment

if page=="Overview":
    risk_banner(assessment); events=db.history()
    sim=st.session_state.get("sim_objects",[]) if st.session_state.input_mode=="SIMULATION" else []
    metric_row(assessment,len(sim),any(x.get("in_zone") for x in sim),len(events))
    st.subheader("System status")
    st.json({"input_mode":st.session_state.input_mode,"video_status":camera.description,"YOLO_status":"loaded" if detector.model else (detector.error or "not loaded"),"audio":"muted" if alarm.muted else (alarm.error or "enabled")})
    st.warning("Risk score is a transparent prioritization rule, not a validated probability of an accident.")
elif page=="Live Monitor":
    st.subheader("Live Monitor")
    source_type=st.radio("Input",["Webcam","Upload video"],horizontal=True)
    upload=st.file_uploader("Upload a video",type=["mp4","avi","mov","mkv"]) if source_type=="Upload video" else None
    cam_index=st.number_input("Webcam index",0,10,0) if source_type=="Webcam" else 0
    start,pause,stop=st.columns(3)
    if start.button("Start",use_container_width=True):
        src=cam_index
        if upload:
            tmp=tempfile.NamedTemporaryFile(delete=False,suffix=Path(upload.name).suffix); tmp.write(upload.getbuffer()); tmp.close(); src=tmp.name
        st.session_state.running=camera.open(src)
        if not st.session_state.running: st.error(camera.description)
    if pause.button("Pause",use_container_width=True): st.session_state.running=False
    if stop.button("Stop",use_container_width=True): st.session_state.running=False; camera.release()
    st.caption(f"Status: {camera.description}. Live sources use REAL_YOLO only; simulations never appear as real video detections.")
    frame_box=st.empty(); details=st.empty()
    if st.session_state.running:
        ok,frame=camera.read()
        if ok:
            output,objects=VideoProcessor(detector,tracker).process(frame,zone,confidence)
            train=st.toggle("Manual train-approach input (MANUAL INPUT)",False,key="manual_train")
            assessment=calculator.assess(objects,train,"MANUAL INPUT" if train else "NOT AVAILABLE")
            st.session_state.last_assessment=assessment; st.session_state.input_mode="REAL VIDEO"
            desc=alert_description(assessment,"REAL YOLO + MANUAL INPUT")
            if assessment.state!="SAFE": db.record_alert_once(assessment,objects,"REAL VIDEO","MANUAL INPUT" if train else "NOT AVAILABLE",train,desc,ALERT_COOLDOWN_SECONDS)
            if assessment.state=="HIGH RISK": alarm.beep("high-risk",ALERT_COOLDOWN_SECONDS)
            frame_box.image(cv2.cvtColor(output,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
            details.dataframe(pd.DataFrame(objects),use_container_width=True)
            st.caption("Live processing active — refreshes automatically while running. Pause or Stop remains available on the next render.")
            # A short rerun cadence processes the next webcam/video frame without a blocking OpenCV loop.
            import time
            time.sleep(0.03)
            st.rerun()
        else: st.session_state.running=False; st.warning(camera.description)
elif page=="Risk":
    risk_banner(assessment); st.subheader("Input provenance")
    source=st.session_state.get("sim_source","NOT AVAILABLE") if st.session_state.input_mode=="SIMULATION" else "MANUAL INPUT / NOT AVAILABLE"
    st.json({"mode":st.session_state.input_mode,"train_source":source,"note":"No train signal is fabricated. Simulation is explicitly labeled."})
elif page=="Alerts & History":
    st.subheader("Event history")
    filt=st.selectbox("Severity",["All","SAFE","CAUTION","HIGH RISK"])
    st.dataframe(pd.DataFrame(db.history(risk=filt)),use_container_width=True,hide_index=True)
    if st.button("Test audible warning"):
        alarm.beep("test",0); st.info(alarm.error or "Test tone requested.")
elif page=="Analytics":
    analytics(db.history())
else:
    st.subheader("Settings & safety boundaries")
    st.write("Configure source in Live Monitor, confidence and polygon in the sidebar. The model weight is downloaded by Ultralytics on first use when internet is available.")
    st.code("streamlit run app.py",language="bash")
    st.error("This educational prototype must not be used as a certified safety system or connected to operational railway infrastructure.")
