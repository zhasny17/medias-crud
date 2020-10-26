from tests.test_login import login
from . import client, TEST_USERNAME, TEST_PASSWORD

#############################################################################
#                               TEST FUNCTIONS                              #
#############################################################################
def test_user(client):
    response = login(client, grant_type='password', username=TEST_USERNAME, password=TEST_PASSWORD)
    at = response.get_json().get('acess_token')

    headers = {'Authorization': 'Bearer: ' + at}

    response = client.get('/users/', headers=headers)
    assert response.status_code == 200

    response = client.get('/users/?page1&pagesize=50', headers=headers)
    assert response.status_code == 200

    response = client.get('/users/?page=f&pagesize=0', headers=headers)
    assert response.status_code == 400

    user_json = {"username": "xablau", "name": "Xablau", "password": "123456"}
    response = client.post('/users/', headers=headers, json=user_json)
    assert response.status_code == 204

    response = client.get('/users/ec77386x-16f4-45f6-8g75-g5e0c75c5339', headers=headers)
    assert response.status_code == 200

    response = client.get('/users/5', headers=headers)
    assert response.status_code == 404

    user_edit = {"username": "xablau1", "name": "Xablau1"}
    response = client.put('/users/ec77386x-16f4-45f6-8g75-g5e0c75c5339', headers=headers, json=user_edit)
    assert response.status_code == 204

    response = login(client, grant_type='password', username='xablau1', password='qpalzm')
    at = response.get_json().get('acess_token')
    change_pass_obj = {'current_password': 'qpalzm', 'new_password':'pqlamz'}
    response = client.post('/users/change/password', headers={'Authorization': 'Bearer: ' + at}, json=change_pass_obj)
    assert response.status_code == 204

    response = client.put('/users/5', headers=headers, json=user_edit)
    assert response.status_code == 404

    response = client.delete('/users/ec77386x-16f4-45f6-8g75-g5e0c75c5339', headers=headers)
    assert response.status_code == 204

    response = client.get('/users/ec77386x-16f4-45f6-8g75-g5e0c75c5339', headers=headers)
    assert response.status_code == 404

    response = client.delete('/users/5', headers=headers)
    assert response.status_code == 404
