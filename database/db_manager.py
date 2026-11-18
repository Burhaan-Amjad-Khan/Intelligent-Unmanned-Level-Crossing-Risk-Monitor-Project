import sqlite3
from contextlib import closing
from config.settings import DATABASE_PATH

class DatabaseManager:
    def __init__(self, path=DATABASE_PATH):
        self.path = path
    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as con:
            con.execute('''CREATE TABLE IF NOT EXISTS events(
              id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, input_mode TEXT NOT NULL,
              object_class TEXT, confidence REAL, location TEXT, zone_status TEXT, duration REAL,
              risk_level TEXT NOT NULL, risk_score INTEGER NOT NULL, train_source TEXT, train_active INTEGER,
              alert_description TEXT)''')
            con.commit()
    def record(self, assessment, objects, input_mode, train_source, train_active, description):
        self.initialize(); objects = objects or [{}]
        try:
            with closing(sqlite3.connect(self.path)) as con:
                for obj in objects:
                    con.execute('''INSERT INTO events(timestamp,input_mode,object_class,confidence,location,zone_status,duration,risk_level,risk_score,train_source,train_active,alert_description)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (assessment.timestamp.isoformat(timespec="seconds"), input_mode,
                    obj.get("label"), obj.get("confidence"), str(obj.get("bbox", "SIMULATED")), str(obj.get("in_zone",False)),
                    obj.get("duration",0), assessment.state, assessment.score, train_source, int(train_active), description))
                con.commit()
        except sqlite3.Error as exc: raise RuntimeError(f"Database write failed: {exc}") from exc
    def record_alert_once(self, assessment, objects, input_mode, train_source, train_active, description, cooldown_seconds=12):
        """Persist a non-safe alert only once per equivalent state/reason inside its cooldown."""
        self.initialize()
        with closing(sqlite3.connect(self.path)) as con:
            latest = con.execute("SELECT timestamp FROM events WHERE risk_level=? AND alert_description=? ORDER BY id DESC LIMIT 1", (assessment.state, description)).fetchone()
            if latest:
                from datetime import datetime
                try:
                    if (assessment.timestamp - datetime.fromisoformat(latest[0])).total_seconds() < cooldown_seconds:
                        return False
                except ValueError:
                    pass
        self.record(assessment, objects, input_mode, train_source, train_active, description)
        return True
    def history(self, limit=200, risk=None):
        self.initialize()
        with closing(sqlite3.connect(self.path)) as con:
            query="SELECT * FROM events"; args=[]
            if risk and risk != "All": query += " WHERE risk_level=?"; args.append(risk)
            query += " ORDER BY id DESC LIMIT ?"; args.append(limit)
            cols=[x[0] for x in con.execute(query,args).description]
            return [dict(zip(cols,row)) for row in con.execute(query,args).fetchall()]
