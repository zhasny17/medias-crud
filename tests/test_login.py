from . import client, TEST_USERNAME, TEST_PASSWORD


#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################
def login(client, **data):
    response = client.post('/auth/login', json=data)
    return response

def logout(client, token):
    return client.post('/auth/logoff', headers={'Authorization': 'Bearer: ' + token})


#############################################################################
#                               TEST FUNCTIONS                              #
#############################################################################
def test_login(client):
    response = login(client, grant_type='password', username=TEST_USERNAME)
    assert response.status_code == 401

    response = login(client, grant_type='refresh_token', username=TEST_USERNAME)
    assert response.status_code == 401

    response = login(client, grant_type='password', username=TEST_USERNAME, password=TEST_PASSWORD)
    assert response.status_code == 200
    rt = response.get_json().get('refresh_token')

    response = login(client, grant_type='refresh_token', refresh_token=rt)
    assert response.status_code == 200
    token = response.get_json().get('acess_token')

    response = logout(client, token)
    assert response.status_code == 204

    response = login(client, grant_type='XXXX')
    assert response.status_code == 400

    response = login(client, grant_type='refresh_token', refresh_token=rt)
    assert response.status_code == 401