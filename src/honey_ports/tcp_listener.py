"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import socket
import threading
from typing import Iterable

from .alert_trigger import handle_new_attack


def log_attack(ip_address: str, port: int) -> None:
    """Public helper for tests and manual logging."""
    handle_new_attack(ip_address=ip_address, port=port)


def _serve_port(port: int) -> None:
    banner = {
        2222: b"SSH-2.0-OpenSSH_8.2\r\n",
        3306: b"5.7.26-log\r\n",
    }.get(port, b"HoneySense\r\n")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(100)

    while True:
        try:
            conn, addr = s.accept()
            ip = addr[0]
            handle_new_attack(ip_address=ip, port=port)
            try:
                conn.sendall(banner)
            except Exception:
                pass
            finally:
                conn.close()
        except Exception:
            # Keep listener alive regardless of errors
            continue


def start_tcp_listeners(ports: Iterable[int] | None = None) -> None:
    if ports is None:
        ports = [2222, 3306]

    for port in ports:
        t = threading.Thread(target=_serve_port, args=(port,), daemon=True)
        t.start()
