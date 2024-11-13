from run import app
from database.session import run_database
import asyncio
import os

from fastapi.testclient import TestClient

os.environ['ENGINE'] = 'sqlite+aiosqlite:///./database/testdb.db'


client = TestClient(app)

asyncio.new_event_loop().run_until_complete(run_database(reset=True))


def login(username, password):
    response = client.post('/auth/login', json={
        "username": username,
        "password": password
    })

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'

    return response.json()['access_token']


def test_ping():
    response = client.get('/ping')
    assert response.status_code == 200


def test_password_letters_error_register():
    response = client.post('/auth/register', json={
        "username": 'zahardimidov',
        "password": "password"
    })

    assert response.status_code == 400
    assert response.json()['detail'] == 'Password must include numbers'


def test_password_numbers_error_register():
    response = client.post('/auth/register', json={
        "username": 'zahardimidov',
        "password": "12345678"
    })

    assert response.status_code == 400
    assert response.json()['detail'] == 'Password must include letters'


def test_username_min_len_error_register():
    response = client.post('/auth/register', json={
        "username": 'zahar',
        "password": "test12345"
    })

    assert response.status_code == 400
    assert response.json()[
        'detail'] == 'Username should include at least 6 symbols'


def test_password_min_len_error_register():
    response = client.post('/auth/register', json={
        "username": 'zahardimidov',
        "password": "test1"
    })
    assert response.status_code == 400
    assert response.json()[
        'detail'] == 'Password should include at least 6 symbols'


def test_successful_register():
    response = client.post('/auth/register', json={
        "username": 'zahardimidov',
        "password": "qwerty123"
    })

    assert response.status_code == 200
    assert response.json()['detail'] == 'Successfully registered'


def test_incorrect_login():
    response = client.post('/auth/login', json={
        "username": 'zahardimidov',
        "password": "qwerty"
    })

    assert response.status_code == 400
    assert response.json()['detail'] == 'Incorrect username or password'


def test_successful_login():
    token = login('zahardimidov', 'qwerty123')

    assert token is not None


def test_notauthenticated_me():
    response = client.get('/auth/me')
    assert response.status_code == 403


def test_authenticated_me():
    token = login('zahardimidov', 'qwerty123')

    response = client.get('/auth/me', headers={
        'Authorization': 'Bearer ' + token
    })
    assert response.status_code == 200
