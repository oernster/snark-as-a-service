"""The two files a crawler reads before anything else.

Both must be served from the host root to be honoured at all, so a routing
mistake here is invisible in the browser and total to a search engine.
"""


def test_robots_txt_is_served(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200

    assert response.headers.get("content-type").startswith("text/plain")
    assert response.headers.get("cache-control") == "public, max-age=86400"


def test_sitemap_xml_is_served(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200

    assert response.headers.get("content-type").startswith("application/xml")
    assert response.headers.get("cache-control") == "public, max-age=86400"
