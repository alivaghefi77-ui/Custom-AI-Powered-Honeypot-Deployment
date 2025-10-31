"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import os
from datetime import datetime
from typing import Optional
from fpdf import FPDF

from .logger import read_stats, read_attacks, get_paths


def generate_report(output_path: Optional[str] = None) -> str:
    stats = read_stats()
    attacks = read_attacks()

    paths = get_paths()
    os.makedirs(paths['archive'], exist_ok=True)

    if not output_path:
        ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(paths['archive'], f'report_{ts}.pdf')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="HoneySense Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Generated: {datetime.utcnow().isoformat()}Z", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Attacks: {stats.get('total_count', 0)}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Top IPs:", ln=True)
    top_ips = sorted((stats.get('top_ips') or {}).items(), key=lambda x: x[1], reverse=True)[:10]
    for ip, cnt in top_ips:
        pdf.cell(200, 8, txt=f" - {ip}: {cnt}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Country Distribution:", ln=True)
    for c, cnt in (stats.get('by_country') or {}).items():
        pdf.cell(200, 8, txt=f" - {c}: {cnt}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Type Distribution:", ln=True)
    for t, cnt in (stats.get('by_type') or {}).items():
        pdf.cell(200, 8, txt=f" - {t}: {cnt}", ln=True)

    pdf.output(output_path)
    return output_path
