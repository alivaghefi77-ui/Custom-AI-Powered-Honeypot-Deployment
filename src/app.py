"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import os
import threading
from datetime import datetime
from flask import Flask, jsonify, redirect, request
from flask_socketio import SocketIO
from typing import Literal, cast, TypeAlias

from dashboard.dashboard_routes import dashboard_bp
from honey_ports.tcp_listener import start_tcp_listeners
from honey_ports.alert_trigger import handle_new_attack
from notifier.ws_manager import set_socketio, broadcast_stats
from utils.logger import ensure_data_files_exist, read_stats


socketio: SocketIO | None = None

# Define at module scope so it's a valid type alias
AllowedAsync: TypeAlias = Literal['threading', 'eventlet', 'gevent', 'gevent_uwsgi']


def create_app() -> tuple[Flask, SocketIO]:
    ensure_data_files_exist()

    app = Flask(__name__, static_folder=None)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'honey_sense_secret')

    mode_env = os.getenv('ASYNC_MODE', 'threading')
    async_mode: AllowedAsync = 'threading'
    if mode_env in ('threading', 'eventlet', 'gevent', 'gevent_uwsgi'):
        async_mode = cast(AllowedAsync, mode_env)

    sio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)
    set_socketio(sio)

    # Register dashboard routes
    app.register_blueprint(dashboard_bp)

    # Decoy endpoints
    @app.route('/')
    def index():
        return redirect('/dashboard')

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        _log_http_attack('/admin')
        return jsonify({"error": "Unauthorized"}), 403

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Capture attempt metadata only (no real auth)
        _log_http_attack('/login')
        return jsonify({"status": "Login failed"}), 401

    @app.route('/db', methods=['GET'])
    def db():
        _log_http_attack('/db')
        return jsonify({"error": "Database connection failed"}), 500

    @app.route('/api/data', methods=['GET'])
    def api_data():
        _log_http_attack('/api/data')
        return jsonify({"items": [], "message": "No data available"})

    @app.route('/api', methods=['GET'])
    def api_root():
        _log_http_attack('/api')
        return jsonify({
            "endpoints": ["/admin", "/login", "/db", "/api/data", "/metrics", "/dashboard"],
        })

    @app.route('/metrics', methods=['GET'])
    def metrics():
        stats = read_stats()
        return jsonify(stats)

    # Expose socketio to outer scope
    global socketio
    socketio = sio

    return app, sio


def _log_http_attack(path: str) -> None:
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr) or '0.0.0.0'
    except RuntimeError:
        ip = '0.0.0.0'
    port = int(os.getenv('PORT', '8080'))
    method = request.method if request else 'GET'
    handle_new_attack(ip_address=ip, port=port, path=path, method=method)


def _start_background_services() -> None:
    # Start TCP listeners for 2222 and 3306 (port 8080 is used by Flask)
    threading.Thread(target=start_tcp_listeners, args=([2222, 3306],), daemon=True).start()

    # Periodically broadcast stats to dashboard
    def _stats_broadcaster():
        import time
        while True:
            stats = read_stats()
            broadcast_stats(stats)
            time.sleep(10)

    threading.Thread(target=_stats_broadcaster, daemon=True).start()


if __name__ == '__main__':
    app, sio = create_app()
    _start_background_services()

    port = int(os.getenv('PORT', '8080'))
    # eventlet/gevent optional; threading is default when ASYNC_MODE not set
    sio.run(app, host='0.0.0.0', port=port)
