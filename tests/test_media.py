from tests.test_login import login
from . import client, TEST_USERNAME, TEST_PASSWORD

#############################################################################
#                               TEST FUNCTIONS                              #
#############################################################################
def test_media(client):
    response = login(client, grant_type='password', username=TEST_USERNAME, password=TEST_PASSWORD)
    at = response.get_json().get('acess_token')

    headers = {'Authorization': 'Bearer: ' + at}

    media_obj = {'name': 'aula1', 'url': 'https://test', 'duration': 10}
    response = client.post('/medias/', headers=headers, json=media_obj)
    assert response.status_code == 204

    response = client.post('/medias/', headers=headers, json={**media_obj, 'aditionalParameter': 'xxx'})
    assert response.status_code == 400

    response = client.get('/medias/?page=1&pagesize=50', headers=headers)
    assert response.status_code == 200
    media_id = str(response.get_json().get('medias')[0].get('id'))

    response = client.get('/medias/' + media_id, headers=headers)
    assert response.status_code == 200

    response = client.get('/medias/xxx', headers=headers)
    assert response.status_code == 404

    media_obj = {'name': 'aula2', 'url': 'https://test', 'duration': 10}
    response = client.put('/medias/' + media_id, headers=headers, json=media_obj)
    assert response.status_code == 204

    response = client.put('/medias/' + media_id, headers=headers, json={**media_obj, 'aditionalParameter': 'xxx'})
    assert response.status_code == 400

    response = client.delete('/medias/' + media_id, headers=headers)
    assert response.status_code == 204

    response = client.get('/medias/?allmedias=0&page=1&pagesize=50', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json().get('medias')) == 0
