from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RiskAssessment:
    state: str
    score: int
    reason: str
    timestamp: datetime

class RiskCalculator:
    """Transparent rule engine. Score is prioritization only, never accident probability."""
    def assess(self, objects, train_approach=False, train_source="NOT AVAILABLE"):
        in_zone = [o for o in objects if o.get("in_zone")]
        duration = max((float(o.get("duration",0)) for o in in_zone), default=0)
        labels = ", ".join(sorted({str(o.get("label","object")) for o in in_zone}))
        if train_approach and in_zone:
            return RiskAssessment("HIGH RISK", min(100, 80 + min(15,len(in_zone)*5)),
              f"{labels.title()} in danger zone while {train_source.lower()} train approach is active.", datetime.now())
        if in_zone:
            extra = 10 if duration >= 10 else 0
            return RiskAssessment("CAUTION", min(75, 40+len(in_zone)*10+extra),
              f"{labels.title()} occupies the danger zone" + (f" for {duration:.1f}s." if duration else "."), datetime.now())
        if train_approach:
            return RiskAssessment("CAUTION", 30, f"{train_source.title()} train approach warning active; danger zone clear.", datetime.now())
        return RiskAssessment("SAFE", 0, "Danger zone is clear and no train-approach warning is active.", datetime.now())
