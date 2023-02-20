from fastapi.testclient import TestClient


def get_access_token(
    client: TestClient,
    username: str,
    password: str,
):
    payload = "password={}&username={}".format(password, username)
    response = client.post(
        "/auth/token",
        content=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 201
    assert response.json()["access_token"]

    return response.json()["access_token"]
