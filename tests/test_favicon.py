def test_favicon_is_served(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 200

    # FastAPI's FileResponse should return the media type we set
    assert response.headers.get("content-type") == "image/png"

