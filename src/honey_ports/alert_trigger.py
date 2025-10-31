"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import os
from datetime import datetime
from typing import Any, Dict

from intelligence.analyzer import analyzer
from notifier.ws_manager import broadcast_event, broadcast_stats
from notifier.telegram_bot import send_alert
from utils.geoip_lookup import lookup_country
from utils.logger import (
    append_attack_event,
    read_attacks,
    read_stats,
    update_stats,
)
from utils.pdf_reporter import generate_report


def handle_new_attack(ip_address: str, port: int, path: str | None = None, method: str | None = None) -> Dict[str, Any]:
    event: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": ip_address,
        "port": port,
        "path": path or "",
        "method": method or "",
        "country": lookup_country(ip_address),
    }

    # Analyze event via AI
    classification, score = analyzer.analyze_event(event)
    event["classification"] = classification
    event["score"] = float(score)

    # Persist event and update stats
    append_attack_event(event)
    stats = update_stats(event)

    # Broadcast to dashboard
    broadcast_event(event)
    broadcast_stats(stats)

    # Conditional PDF report generation
    try:
        attacks = read_attacks()
        if len(attacks) % 50 == 0:
            generate_report()
    except Exception:
        pass

    # Telegram alert
    try:
        msg = (
            f"HoneySense Alert\n"
            f"IP: {event['ip']} ({event['country']})\n"
            f"Port: {event['port']}\n"
            f"Path: {event.get('path','')}\n"
            f"Type: {event['classification']}\n"
            f"Score: {event['score']:.4f}"
        )
        send_alert(msg)
    except Exception:
        pass

    return event
