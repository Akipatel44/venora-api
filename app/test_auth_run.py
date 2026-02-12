from fastapi.testclient import TestClient
from app.main import app
from app.seed_users import seed


def run_tests():
    # Ensure DB seeded (uses DATABASE_URL from environment)
    seed()
    client = TestClient(app)

    users = [
        ("super@venora.local", "superpass"),
        ("sub@venora.local", "subpass"),
        ("cust@venora.local", "custpass"),
    ]

    for email, pwd in users:
        resp = client.post("/auth/login", data={"username": email, "password": pwd})
        print(email, resp.status_code, resp.json())


if __name__ == "__main__":
    run_tests()
