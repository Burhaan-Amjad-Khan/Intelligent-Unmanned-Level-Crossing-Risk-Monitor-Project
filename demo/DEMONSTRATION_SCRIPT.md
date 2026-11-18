# 3–5 minute demonstration recording script

Do **not** claim simulations are real detections.

1. **0:00–0:20:** Show title, Project ID, and educational/non-operational safety notice.
2. **0:20–0:50:** Overview: explain status and provenance labels.
3. **0:50–1:40:** Live Monitor: select webcam or uploaded footage, Start, show genuine YOLO boxes and zone overlay. If no compatible footage/camera exists, state this honestly on screen.
4. **1:40–2:45:** Run six sidebar simulations: Empty (SAFE), Vehicle (CAUTION), Pedestrian (CAUTION), Remains (CAUTION), Train approach + occupied (HIGH RISK), Zone clears (SAFE). Keep the SIMULATION label visible.
5. **2:45–3:30:** Show risk reason, alert test/mute, event history, and analytics.
6. **3:30–4:00:** Close with limitations: no operational train-control connection, not certified, score not a probability.

Record from the locally running application, then export `demo/demonstration.mp4` at 1280×720 H.264, CRF 28–30 to aim below 15 MB. This file is intentionally not fabricated in advance.
