"""
HoneySense tests — Authored by Ali Vaghefi (Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui)
"""
from intelligence.analyzer import analyzer


def test_ai_analyzer_classification_labels():
    event = {
        "timestamp": "2025-01-01T00:00:00Z",
        "ip": "10.0.0.1",
        "port": 2222,
        "path": "/",
        "method": "GET",
        "country": "Unknown",
    }
    label, score = analyzer.analyze_event(event)
    assert label in {"Suspicious", "Scanner", "BruteForce", "Normal"}
