"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
from __future__ import annotations
from typing import Any, Dict
from flask_socketio import SocketIO

_socketio: SocketIO | None = None

def set_socketio(socketio: SocketIO) -> None:
    global _socketio
    _socketio = socketio


def broadcast_event(event: Dict[str, Any]) -> None:
    if _socketio is None:
        return
    try:
        _socketio.emit('attack_event', event, broadcast=True)
    except TypeError:
        # Some async modes do not accept broadcast kwarg
        _socketio.emit('attack_event', event)


def broadcast_stats(stats: Dict[str, Any]) -> None:
    if _socketio is None:
        return
    try:
        _socketio.emit('stats_update', stats, broadcast=True)
    except TypeError:
        _socketio.emit('stats_update', stats)
