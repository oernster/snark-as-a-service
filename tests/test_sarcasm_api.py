def test_get_sarcastic_quote(client):
    response = client.get("/api/v1/sarcasm/")
    assert response.status_code == 200

    data = response.json()
    assert "text" in data
    assert isinstance(data["text"], str)
    assert len(data["text"]) > 0
