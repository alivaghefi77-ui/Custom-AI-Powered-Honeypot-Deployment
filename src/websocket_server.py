"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
from __future__ import annotations
from flask_socketio import SocketIO

# This module can be extended for custom Socket.IO event handlers if needed.

_socketio: SocketIO | None = None

def init_socketio(socketio: SocketIO) -> None:
    global _socketio
    _socketio = socketio


def get_socketio() -> SocketIO | None:
    return _socketio
