from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] in {'ok', 'degraded'}


def test_settings_roundtrip():
    current = client.get('/api/settings').json()
    payload = {**current, 'confidence_cutoff': 61}
    updated = client.put('/api/settings', json=payload)
    assert updated.status_code == 200
    assert updated.json()['confidence_cutoff'] == 61


def test_ws_message_format():
    with client.websocket_connect('/ws/stream') as ws:
        ws.send_text('ping')
