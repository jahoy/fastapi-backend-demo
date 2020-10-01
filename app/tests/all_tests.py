from starlette.testclient import TestClient
from run import app
from utils.db import fetch, execute
import asyncio
from utils.security import get_hashed_password


client = TestClient(app)
loop = asyncio.get_event_loop()


def insert_user(username, password):
    query = """insert into users(username,password) values(:username,:password)"""
    hashed_password = get_hashed_password(password)
    values = {"username": username, "password": hashed_password}

    loop.run_until_complete(execute(query, False, values))


def check_personel_user(username, mail):
    query = """select * from personel where username=:username and mail=:mail"""
    values = {"username": username, "mail": mail}

    result = loop.run_until_complete(fetch(query, True, values))

    if result is None:
        return False

    return True


def get_auth_header():
    insert_user("test", "test")
    response = client.post("/token", dict(username="test", password="test"))
    jwt_token = response.json()["access_token"]

    auth_header = {"Authorization": f"Bearer {jwt_token}"}
    return auth_header


def clear_db():
    query1 = """delete from users;"""
    query2 = """delete from authors;"""
    query3 = """delete from books;"""
    query4 = """delete from personel;"""

    loop.run_until_complete(execute(query1, False))
    loop.run_until_complete(execute(query2, False))
    loop.run_until_complete(execute(query3, False))
    loop.run_until_complete(execute(query4, False))


def test_token_successful():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass1"))

    assert response.status_code == 200
    assert "access_token" in response.json()

    clear_db()


def test_token_unauthorized():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass"))

    assert response.status_code == 401

    clear_db()


def test_post_user():
    auth_header = get_auth_header()

    user_dict = {
        "name": "user1",
        "password": "secret",
        "mail": "a@b.com",
        "role": "admin",
    }

    response = client.post("/v1/user", json=user_dict, headers=auth_header)

    assert response.status_code == 201
    assert check_personel_user("user1", "a@b.com") == True

    clear_db()


def test_post_user_wrong_email():
    auth_header = get_auth_header()

    user_dict = {
        "name": "user1",
        "password": "secret",
        "mail": "invalid",
        "role": "admin",
    }

    response = client.post("/v1/user", json=user_dict, headers=auth_header)

    assert response.status_code == 422

    clear_db()
