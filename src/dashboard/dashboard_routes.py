"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
from __future__ import annotations
from flask import Blueprint, render_template
from utils.logger import read_stats


dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')


@dashboard_bp.route('/dashboard')
def dashboard_view():
    return render_template('index.html')
