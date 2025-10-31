"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
from __future__ import annotations
import json
import os
import threading
from datetime import datetime
from typing import Any, Dict, List

_DATA_LOCK = threading.Lock()
_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
_ATTACKS_FILE = os.path.join(_BASE_DIR, 'attacks_log.json')
_STATS_FILE = os.path.join(_BASE_DIR, 'threat_stats.json')
_ARCHIVE_DIR = os.path.join(_BASE_DIR, 'archived_reports')


def ensure_data_files_exist() -> None:
    os.makedirs(_BASE_DIR, exist_ok=True)
    os.makedirs(_ARCHIVE_DIR, exist_ok=True)
    with _DATA_LOCK:
        if not os.path.exists(_ATTACKS_FILE):
            with open(_ATTACKS_FILE, 'w') as f:
                json.dump([], f)
        if not os.path.exists(_STATS_FILE):
            with open(_STATS_FILE, 'w') as f:
                json.dump(_default_stats(), f)


def _default_stats() -> Dict[str, Any]:
    return {
        "total_count": 0,
        "per_minute": {},
        "top_ips": {},
        "by_country": {},
        "by_type": {},
    }


def append_attack_event(event: Dict[str, Any]) -> None:
    ensure_data_files_exist()
    with _DATA_LOCK:
        data = []
        try:
            with open(_ATTACKS_FILE, 'r') as f:
                data = json.load(f)
        except Exception:
            data = []
        data.append(event)
        with open(_ATTACKS_FILE, 'w') as f:
            json.dump(data, f, indent=2)


def read_attacks() -> List[Dict[str, Any]]:
    ensure_data_files_exist()
    with _DATA_LOCK:
        try:
            with open(_ATTACKS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return []


def get_attack_count() -> int:
    return len(read_attacks())


def read_stats() -> Dict[str, Any]:
    ensure_data_files_exist()
    with _DATA_LOCK:
        try:
            with open(_STATS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return _default_stats()


def update_stats(event: Dict[str, Any]) -> Dict[str, Any]:
    ensure_data_files_exist()
    with _DATA_LOCK:
        stats = read_stats()
        stats["total_count"] = int(stats.get("total_count", 0)) + 1

        # Per-minute bucket
        ts = event.get('timestamp', '')
        minute_key = ts[:16]  # YYYY-MM-DDTHH:MM
        per_min = stats.get('per_minute', {})
        per_min[minute_key] = int(per_min.get(minute_key, 0)) + 1
        stats['per_minute'] = per_min

        # Top IPs
        ip = event.get('ip', 'unknown')
        top_ips = stats.get('top_ips', {})
        top_ips[ip] = int(top_ips.get(ip, 0)) + 1
        stats['top_ips'] = top_ips

        # By country
        c = event.get('country', 'Unknown')
        by_country = stats.get('by_country', {})
        by_country[c] = int(by_country.get(c, 0)) + 1
        stats['by_country'] = by_country

        # By type
        t = event.get('classification', 'Unknown')
        by_type = stats.get('by_type', {})
        by_type[t] = int(by_type.get(t, 0)) + 1
        stats['by_type'] = by_type

        with open(_STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
        return stats


def get_paths() -> Dict[str, str]:
    return {
        "attacks": _ATTACKS_FILE,
        "stats": _STATS_FILE,
        "archive": _ARCHIVE_DIR,
    }
