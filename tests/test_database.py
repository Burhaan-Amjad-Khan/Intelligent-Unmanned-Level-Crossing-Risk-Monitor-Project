from datetime import datetime
from database.db_manager import DatabaseManager
from risk_engine.risk_calculator import RiskAssessment

def test_database_roundtrip(tmp_path):
    db=DatabaseManager(tmp_path/"test.db"); event=RiskAssessment("CAUTION",50,"car in zone",datetime.now())
    db.record(event,[{"label":"car","confidence":.9,"in_zone":True,"duration":2}],"SIMULATION","SIMULATED TRAIN APPROACH",False,"test")
    rows=db.history(); assert len(rows)==1 and rows[0]["object_class"]=="car" and rows[0]["input_mode"]=="SIMULATION"

def test_alert_deduplication(tmp_path):
    db=DatabaseManager(tmp_path/"test.db"); event=RiskAssessment("HIGH RISK",85,"car in zone",datetime.now())
    assert db.record_alert_once(event,[{"label":"car","in_zone":True}],"REAL VIDEO","MANUAL INPUT",True,"same",60)
    assert not db.record_alert_once(event,[{"label":"car","in_zone":True}],"REAL VIDEO","MANUAL INPUT",True,"same",60)
    assert len(db.history())==1
