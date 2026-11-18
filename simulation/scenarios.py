SCENARIOS = {
 "Empty / normal crossing": ([], False, "SIMULATED TRAIN APPROACH"),
 "Vehicle enters danger zone": ([{"label":"car","confidence":1.0,"in_zone":True,"duration":0,"source":"SIMULATED"}], False, "SIMULATED TRAIN APPROACH"),
 "Pedestrian enters danger zone": ([{"label":"person","confidence":1.0,"in_zone":True,"duration":0,"source":"SIMULATED"}], False, "SIMULATED TRAIN APPROACH"),
 "Obstacle remains in zone": ([{"label":"truck","confidence":1.0,"in_zone":True,"duration":15,"source":"SIMULATED"}], False, "SIMULATED TRAIN APPROACH"),
 "Train approach + occupied zone": ([{"label":"car","confidence":1.0,"in_zone":True,"duration":4,"source":"SIMULATED"}], True, "SIMULATED TRAIN APPROACH"),
 "Zone clears": ([], False, "SIMULATED TRAIN APPROACH"),
}
def scenario(name): return SCENARIOS[name]
