from app import create_app


def test_healthz():
    app = create_app()
    client = app.test_client()
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.get_json().get('status') == 'ok'


def test_livez():
    app = create_app()
    client = app.test_client()
    resp = client.get('/livez')
    assert resp.status_code == 200
    assert resp.get_json().get('alive') is True


