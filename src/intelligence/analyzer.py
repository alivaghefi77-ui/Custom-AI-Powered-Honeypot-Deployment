"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
from __future__ import annotations
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.ensemble import IsolationForest

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
ATTACKS_FILE = os.path.join(DATA_DIR, 'attacks_log.json')
MODEL_FILE = os.path.join(os.path.dirname(__file__), 'model.pkl')


@dataclass
class AnomalyAnalyzer:
    model: IsolationForest
    events_since_train: int = 0

    def _default_model(self) -> IsolationForest:
        return IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

    def _load_model(self) -> IsolationForest:
        if os.path.exists(MODEL_FILE):
            try:
                import joblib
                return joblib.load(MODEL_FILE)
            except Exception:
                pass
        return self._default_model()

    def _save_model(self) -> None:
        try:
            import joblib
            joblib.dump(self.model, MODEL_FILE)
        except Exception:
            pass

    def _extract_feature_vector(self, event: Dict[str, Any]) -> np.ndarray:
        # Basic features: hour of day, port, ip repetition count
        hour = 0
        try:
            hour = datetime.fromisoformat(event["timestamp"].replace("Z", "")).hour
        except Exception:
            pass
        port = int(event.get("port", 0))
        ip_rep = self._ip_repetition(event.get("ip", ""))
        return np.array([hour, port, ip_rep], dtype=float)

    def _ip_repetition(self, ip: str) -> int:
        try:
            if not os.path.exists(ATTACKS_FILE):
                return 0
            with open(ATTACKS_FILE, 'r') as f:
                data = json.load(f)
            return sum(1 for e in data if e.get('ip') == ip)
        except Exception:
            return 0

    def _load_training_matrix(self) -> np.ndarray:
        if not os.path.exists(ATTACKS_FILE):
            return np.empty((0, 3))
        try:
            with open(ATTACKS_FILE, 'r') as f:
                data = json.load(f)
            X = [self._extract_feature_vector(e) for e in data]
            return np.vstack(X) if X else np.empty((0, 3))
        except Exception:
            return np.empty((0, 3))

    def _maybe_retrain(self) -> None:
        self.events_since_train += 1
        if self.events_since_train < 50:
            return
        X = self._load_training_matrix()
        if X.shape[0] >= 20:
            try:
                self.model.fit(X)
                self._save_model()
            except Exception:
                pass
        self.events_since_train = 0

    def analyze_event(self, event: Dict[str, Any]) -> Tuple[str, float]:
        # Ensure model is ready
        if not hasattr(self, 'model') or self.model is None:
            self.model = self._load_model()

        x = self._extract_feature_vector(event).reshape(1, -1)
        # Fallback: if model not yet fitted, pretend normal with low anomaly score
        score = -0.1
        label = 1
        try:
            score = float(self.model.decision_function(x)[0])
            label = int(self.model.predict(x)[0])  # -1 anomaly, 1 normal
        except Exception:
            pass

        ip_rep = int(self._ip_repetition(event.get('ip', '')))
        port = int(event.get('port', 0))

        if label == -1:
            if ip_rep >= 5:
                classification = 'BruteForce'
            elif port in (2222, 3306):
                classification = 'Scanner'
            else:
                classification = 'Suspicious'
        else:
            classification = 'Normal'

        # Schedule potential retraining
        self._maybe_retrain()
        return classification, score


# Global singleton
analyzer = AnomalyAnalyzer(model=IsolationForest(n_estimators=100, contamination=0.1, random_state=42))
