from risk_engine.risk_calculator import RiskCalculator

def test_safe_when_clear(): assert RiskCalculator().assess([]).state == "SAFE"
def test_caution_when_object_inside():
    result=RiskCalculator().assess([{"label":"car","in_zone":True,"duration":0}])
    assert result.state == "CAUTION" and result.score == 50
def test_caution_train_warning_when_clear(): assert RiskCalculator().assess([],True,"MANUAL INPUT").state == "CAUTION"
def test_high_risk_requires_train_and_occupancy():
    result=RiskCalculator().assess([{"label":"person","in_zone":True,"duration":1}],True,"SIMULATED TRAIN APPROACH")
    assert result.state == "HIGH RISK" and result.score >= 80
