## HoneySense

An AI‑driven honeypot that detects, analyzes, visualizes, and alerts on suspicious activity in real time — built for security engineers who want signal, not noise.

### Why HoneySense?
- **See attacks as they happen**: Real-time dashboard powered by Socket.IO and Chart.js.
- **Lightweight AI**: IsolationForest flags anomalies like scanners and brute force attempts.
- **Multi-surface deception**: Decoy HTTP endpoints plus TCP listeners (SSH/MySQL simulators).
- **Actionable alerts**: Telegram notifications and auto-generated PDF reports.
- **Simple to run**: Works locally or in Docker. One command to spin up.

### How it works (at a glance)
1) Attacker hits a decoy HTTP endpoint or TCP port 2222/3306  
2) Event is logged to `data/attacks_log.json`  
3) AI analyzer classifies the behavior (Normal / Suspicious / Scanner / BruteForce)  
4) Stats get updated and broadcast in real time to the dashboard  
5) Telegram alert is sent (optional), and periodic PDF reports are generated

---

## Tech Stack
- **Language**: Python (>=3.10)
- **Framework**: Flask + Flask-SocketIO
- **Category**: Security / Honeypot / AI

## Features
- **Deceptive Endpoints**: `/admin`, `/login`, `/db`, `/api/data`, `/api`, `/metrics`
- **Multi-Port Honeypot**: TCP listeners on `2222` (SSH) and `3306` (MySQL); HTTP traffic on `8080` via Flask is also logged as attacks.
- **AI Analyzer**: IsolationForest-based anomaly detection with incremental retraining every 50 events.
- **Real-Time Dashboard**: Live charts for attacks/minute, top IPs, and country distribution.
- **Alerts**: Telegram alerts with optional DRY RUN for safe testing.
- **Reports**: PDF summaries saved under `data/archived_reports/`.

## Project Structure
```
src/
  app.py
  websocket_server.py
  honey_ports/
    tcp_listener.py
    deception_endpoints.py
    alert_trigger.py
  intelligence/
    analyzer.py
    model.pkl
  dashboard/
    templates/index.html
    static/styles.css
    static/chart.js
    dashboard_routes.py
  notifier/
    telegram_bot.py
    ws_manager.py
  utils/
    geoip_lookup.py
    logger.py
    pdf_reporter.py
  tests/
    test_tcp_listener.py
    test_ai_analysis.py
    test_dashboard.py

data/
  attacks_log.json
  threat_stats.json
  archived_reports/

Dockerfile
docker-compose.yml
requirements.txt
LICENSE
.env.example
README.md
```

## Quick start
### Run with Docker (recommended)
```bash
docker compose up --build -d
# Then open: http://localhost:8080/dashboard
```

### Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional: avoid eventlet issues on new Pythons
export ASYNC_MODE=threading
python src/app.py
```
Open `http://localhost:8080/dashboard`

## Configure
Copy `.env.example` to `.env` and set your values:
```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
FLASK_ENV=production
SECRET_KEY=honey_sense_secret
PORT=8080
TELEGRAM_DRY_RUN=1
```
- Set `TELEGRAM_DRY_RUN=0` when ready to send real alerts.
- For GeoIP, put `GeoLite2-Country.mmdb` in `data/` or set `GEOIP_DB` to its path.

## Testing
```bash
pip install -r requirements.txt
pytest -q
```

## Troubleshooting
- **Import errors (flask, flask_socketio) in IDE**  
  Create a venv and point your IDE to it:  
  `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`  
  In VSCode/Cursor: Python: Select Interpreter → `.venv/bin/python`

- **Eventlet issues on newer Python (e.g., 3.13)**  
  Run with threading mode: `export ASYNC_MODE=threading`

- **Port 8080 already in use**  
  Change `PORT` in `.env` or free the port: `lsof -i :8080`

- **Static assets not loading**  
  The dashboard uses Flask blueprint static paths; hard refresh (Ctrl/Cmd+Shift+R) if cached.

## Data & Privacy
- Logs are stored under `data/` on the host and include IP addresses and basic metadata.
- Use in controlled environments and comply with local laws and network policies.

## Security Notes
- HoneySense is a honeypot; do not deploy it on production networks without clear segmentation and monitoring.
- If exposing to the internet, consider additional hardening (firewalls, rate limits, WAF).

## Roadmap
- Deeper ML features and supervised classification
- Slack and email alert channels
- External ELK stack integration
- Fake login form credential capture

## Creat .env yourself
- TELEGRAM_BOT_TOKEN=your_token_here
- TELEGRAM_CHAT_ID=your_chat_id_here
- FLASK_ENV=production
- SECRET_KEY=honey_sense_secret
- PORT=8080
- TELEGRAM_DRY_RUN=1


### 🧠 Author & Maintainer
**Ali Vaghefi** — Backend & Network Security Engineer  
🛡️ Passionate about secure software, DevSecOps, and ethical development.  
[Arc.dev](https://arc.dev/@alivaghefi77ui?preview=1) | [GitHub](https://github.com/alivaghefi77-ui)

## License
MIT — see `LICENSE` for details.
