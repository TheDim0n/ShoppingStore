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


def get_headers(
    client: TestClient,
    username: str,
    password: str,
) -> dict:
    access_token = get_access_token(client, username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
