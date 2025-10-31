"""
HoneySense tests — Authored by Ali Vaghefi (Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui)
"""
from src.app import create_app


def test_flask_endpoints():
    app, sio = create_app()
    client = app.test_client()

    r = client.get('/login')
    assert r.status_code in (200, 401)

    r = client.get('/db')
    assert r.status_code in (200, 500)

    r = client.get('/api/data')
    assert r.status_code == 200

    r = client.get('/dashboard')
    assert r.status_code == 200
