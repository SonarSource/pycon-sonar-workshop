def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Pokedex</h1>\n" in response.data


def test_subscribe(client):
    response = client.post("/subscribe", data={"email": "blah@example.com"})
    assert response.status_code == 302
