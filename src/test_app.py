import sys
import os
import random
import string
from models import Patient, User
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jwt
from src.core.settings.app import db
try:
    from src.main import app
except ImportError as e:
    print("ImportError:", e)
import pytest
import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def token(client):
    token = jwt.encode({
        'user': 'testuser',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@pytest.fixture
def create_patient():
    characters = string.ascii_letters
    patient_name = ''.join(random.choice(characters) for _ in range(5))
    email = ''.join(random.choice(characters) for _ in range(7))

    patient = Patient(name=patient_name, email=email, phone='+13432543623')
    db.session.add(patient)
    db.session.commit()
    yield patient

    db.session.delete(patient)
    db.session.commit(patient)

def test_dashboard(client):
    response = client.get('/')
    print('Response JSON:', response.json)
    print('Response Data:', response.data)
    print(response.headers)
    assert response.status_code == 200

def test_register(client):
    characters = string.ascii_letters
    username = ''.join(random.choice(characters) for _ in range(5))
    email = ''.join(random.choice(characters) for _ in range(7))

    response = client.post(
        '/api/register',
        headers={
            'Content-Type': 'application/json'
        },
        json={
            'name': username,
            'email': f'{email}@test.com',
            'password': 'Eur3uiq74$ui'
        }
    )

    assert response.status_code == 201

def test_login(client):
    response = client.post('/api/login', json={
        'email': 'testuser@test.com',
        'password': 'Eur3uiq74$ui'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)

    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_get_current_user(client, token):
    response = client.get('/api/current_user', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200

def test_add_patient(client, token):
    characters = string.ascii_letters
    patient_name = ''.join(random.choice(characters) for _ in range(5))
    email = ''.join(random.choice(characters) for _ in range(7))

    response = client.post('/api/patients', headers = {
        'Authorization': f'Bearer {token}'
    }, json={
        'name': patient_name,
        'email': f'{email}@email.com',
        'phone': '+134523452345'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)

    assert response.status_code == 201

def test_read_patients(client, token):
    response = client.get('/api/patients', headers = {
        'Authorization': f'Bearer {token}'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)

    assert response.status_code == 200
    assert 'data' in response.get_json()

def test_read_patient(client, token, create_patient):
    patient_id = create_patient.id
    response = client.get(f'/api/patients/{patient_id}', headers = {
        'Authorization': f'Bearer {token}'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)

    assert response.status_code == 200
    assert 'data' in response.get_json()

def test_update_patient(client, token, create_patient):
    patient_id = create_patient.id

    response = client.put(f'/api/patients/{patient_id}', headers = {
        'Authorization': f'Bearer {token}'
    }, json={
        'name':'new_name',
        'password': 'newPassword123!',
        'email': 'newemail@test.com'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)

    assert response.status_code == 200
    assert 'data' in response.get_json()

def test_delete_patient(client, token, create_patient):
    patient_id = create_patient.id

    response = client.delete(f'/api/patients/{patient_id}', headers = {
        'Authorization': f'Bearer {token}'
    })
    print('Response JSON:', response.json)
    print('Response Data:', response.data)
    assert response.status_code == 200
    assert 'data' in response.get_json()
