def test_ping(client):
    res = client.get("/api/v1/ping")
    assert res.status_code == 200
    assert res.get_json() == {"message": "pong"}
