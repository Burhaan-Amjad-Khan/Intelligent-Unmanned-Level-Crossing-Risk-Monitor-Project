from detection.detector import Detection
from detection.object_tracker import CentroidTracker

def test_tracker_preserves_id_for_overlap():
    tracker=CentroidTracker(); first=tracker.update([Detection("car",.9,(0,0,100,100))])[0]
    second=tracker.update([Detection("car",.9,(5,5,105,105))])[0]
    assert first.track_id==second.track_id
