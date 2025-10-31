"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import os
from typing import Optional


def lookup_country(ip_address: str) -> str:
    """Return country name for an IP, or 'Unknown' if DB not present.
    Looks for MaxMind GeoLite2 Country DB path via GEOIP_DB or data/GeoLite2-Country.mmdb
    """
    db_path = os.getenv('GEOIP_DB')
    if not db_path:
        base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        db_path = os.path.join(base, 'GeoLite2-Country.mmdb')

    if not os.path.exists(db_path):
        return 'Unknown'

    try:
        import geoip2.database
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip_address)
            return response.country.name or 'Unknown'
    except Exception:
        return 'Unknown'
