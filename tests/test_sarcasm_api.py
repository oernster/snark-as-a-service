def test_get_sarcastic_quote(client):
    response = client.get("/api/v1/sarcasm/")
    assert response.status_code == 200

    assert response.headers.get("content-type") == "text/plain; charset=utf-8"
    assert isinstance(response.text, str)
    assert len(response.text) > 0
