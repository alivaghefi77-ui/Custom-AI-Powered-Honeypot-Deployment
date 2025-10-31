"""
HoneySense tests — Authored by Ali Vaghefi (Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui)
"""
import os
import json

# Ensure data files exist in test runs
from utils.logger import ensure_data_files_exist
ensure_data_files_exist()

from honey_ports.tcp_listener import log_attack


def test_attack_detection():
    log_attack("127.0.0.1", 8080)
    attacks_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'attacks_log.json')
    with open(attacks_file) as f:
        data = f.read()
    assert "127.0.0.1" in data
