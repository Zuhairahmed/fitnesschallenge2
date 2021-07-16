from animal_adoption import app, User, UserDetail
import pytest
from flask import json

USERNAME = 'test@test.com'
PASSWORD = 'test'

def create_user(client, request_obj):
    return client.post(
        '/create-user-with-all-details',
        data=json.dumps(request_obj),
        content_type='application/json',
    )

def create_new_adopter(client):
    request_obj = {
        'username': USERNAME,
        'password': PASSWORD,
        'firstName': 'Bob',
        'lastName': 'Ross',
        'userType': 'adopter',
        'shelterName': '',
        'dispositions': '',
        'goodWithAnimals': True,
        'goodWithChildren': False,
        'animalLeashed': False,
        'animalPreference': 'dog',
    }

    return create_user(client, request_obj)

def create_new_shelter_worker(client):
    request_obj = {
        'username': USERNAME,
        'password': PASSWORD,
        'firstName': 'Bob',
        'lastName': 'Ross',
        'userType': 'shelter worker',
        'shelterName': 'Save a Pet',
        'dispositions': '',
        'goodWithAnimals': None,
        'goodWithChildren': None,
        'animalLeashed': None,
        'animalPreference': '',
    }

    return create_user(client, request_obj)

def test_home_route(client):        
    response = client.get('/')
    assert response.status_code == 200

def test_create_new_adopter(client):        
    response = create_new_adopter(client)
    assert response.status_code == 200

def test_login_as_adopter(client):        
    create_new_adopter(client)
    response = client.post(
        '/login',
        data=json.dumps({'username': USERNAME, 'password': PASSWORD}),
        content_type='application/json',
    )
    assert response.status_code == 200

def test_login_without_username_failed(client):        
    create_new_adopter(client)
    response = client.post(
        '/login',
        data=json.dumps({'username': None, 'password': PASSWORD}),
        content_type='application/json',
    )
    assert response.status_code == 400

def test_login_without_username_failed(client):        
    create_new_adopter(client)
    response = client.post(
        '/login',
        data=json.dumps({'username': None, 'password': PASSWORD}),
        content_type='application/json',
    )
    assert response.status_code == 400

def test_login_without_password_failed(client):        
    create_new_adopter(client)
    response = client.post(
        '/login',
        data=json.dumps({'username': USERNAME, 'password': None}),
        content_type='application/json',
    )
    assert response.status_code == 400

def test_login_with_invalid_data_failed(client):        
    create_new_adopter(client)
    with pytest.raises(ValueError):
        client.post(
            '/login',
            data=json.dumps({'username': 'badusername', 'password': 'badpassword'}),
            content_type='application/json',
    )

def test_get_adopter_user_details(client):        
    create_new_adopter(client)
    client.post(
        '/login',
        data=json.dumps({'username': USERNAME, 'password': PASSWORD}),
        content_type='application/json',
    )
    response = client.get(
        '/get-user-details',
        content_type='application/json',
    )

    data = json.loads(response.data)['message']
    assert data['userType'] == 'adopter'
    assert data['username'] == USERNAME
    assert data['firstName'] == 'Bob'
    assert data['lastName'] == 'Ross'
    assert 'animalPreference' in data
    assert 'dispositions' in data
    assert response.status_code == 200

def test_create_new_shelter_worker(client):        
    response = create_new_shelter_worker(client)
    assert response.status_code == 200

def test_get_shelter_worker_details(client):        
    create_new_shelter_worker(client)
    client.post(
        '/login',
        data=json.dumps({'username': USERNAME, 'password': PASSWORD}),
        content_type='application/json',
    )
    response = client.get(
        '/get-user-details',
        content_type='application/json',
    )

    data = json.loads(response.data)['message']
    assert data['userType'] == 'shelter worker'
    assert data['username'] == USERNAME
    assert data['firstName'] == 'Bob'
    assert data['lastName'] == 'Ross'
    assert 'animalPreference' not in data
    assert 'dispositions' not in data
    assert response.status_code == 200

def login_as_admin(client):
    client.post(
        '/login',
        data=json.dumps({'username': 'jeandoe@abc.com', 'password': 'test3'}),
        content_type='application/json',
    )
    return 'jeandoe@abc.com'

def test_login_as_administrator(client):        
    login_as_admin(client)
    response = client.get(
        '/get-user-details',
        content_type='application/json',
    )

    data = json.loads(response.data)['message']
    assert data['userType'] == 'administrator'
    assert data['username'] == 'jeandoe@abc.com'
    assert response.status_code == 200

def test_delete_user(client):        
    login_as_admin(client)

    assert User.get_username_by_id(1) != None

    response = client.delete(
        '/users/1',
        content_type='application/json',
    )

    data = json.loads(response.data)['message']
    assert data == 'Delete succeeded'
    assert User.get_username_by_id(1) == None
    assert response.status_code == 200

def test_admin_cannot_delete_itself(client):        
    admin_username = login_as_admin(client)

    response = client.delete(
        '/users/' + str(User.get_id_by_username(admin_username)),
        content_type='application/json',
    )

    message = json.loads(response.data)['message']
    assert message == 'You are not allowed to delete yourself'
    assert User.get_id_by_username(admin_username) != None
    assert response.status_code == 403

def test_non_admin_cannot_delete_user(client):        
    create_new_shelter_worker(client)
    client.post(
        '/login',
        data=json.dumps({'username': USERNAME, 'password': PASSWORD}),
        content_type='application/json',
    )

    response = client.delete(
        '/users/1',
        content_type='application/json',
    )

    message = json.loads(response.data)['message']
    assert message == 'You are not allowed to delete other users'
    assert response.status_code == 403