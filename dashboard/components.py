import pandas as pd
import plotly.express as px
import streamlit as st

COLORS={"SAFE":"#16a34a","CAUTION":"#f59e0b","HIGH RISK":"#dc2626"}
def risk_banner(assessment):
    color=COLORS[assessment.state]
    st.markdown(f'''<div style="border-left:8px solid {color};background:#111827;padding:18px 22px;border-radius:8px">
    <span style="font-size:12px;color:#9ca3af">CURRENT RISK PRIORITY</span><br><b style="color:{color};font-size:28px">{assessment.state} — {assessment.score}/100</b><br>{assessment.reason}</div>''',unsafe_allow_html=True)
def metric_row(assessment, object_count, occupied, alert_count):
    a,b,c,d=st.columns(4); a.metric("Risk score",f"{assessment.score}/100"); b.metric("Objects",object_count); c.metric("Zone occupied","YES" if occupied else "NO"); d.metric("Recorded events",alert_count)
def analytics(events):
    if not events: st.info("No recorded events yet."); return
    df=pd.DataFrame(events); df["timestamp"]=pd.to_datetime(df["timestamp"])
    left,right=st.columns(2)
    with left: st.plotly_chart(px.histogram(df,x="risk_level",color="risk_level",color_discrete_map=COLORS,title="Risk distribution"),use_container_width=True)
    with right: st.plotly_chart(px.line(df.sort_values("timestamp"),x="timestamp",y="risk_score",color="risk_level",color_discrete_map=COLORS,title="Risk score timeline"),use_container_width=True)
    st.plotly_chart(px.histogram(df.dropna(subset=["object_class"]),x="object_class",title="Detected / simulated object classes"),use_container_width=True)
