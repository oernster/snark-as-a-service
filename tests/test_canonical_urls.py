"""The site must publish exactly one indexable URL for the homepage.

A second URL serving identical content is reported by search engines as a
duplicate, so the legacy /sarcasm alias redirects permanently to the root.
"""

from fastapi import status


def test_sarcasm_alias_redirects_permanently_to_root(client):
    response = client.get("/sarcasm", follow_redirects=False)

    assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
    assert response.headers["location"] == "/"


def test_root_is_served_directly(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == status.HTTP_200_OK
    assert 'rel="canonical" href="https://www.snarkapi.com/"' in response.text
