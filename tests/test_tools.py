from tests.test_login import login
from . import client, TEST_USERNAME, TEST_PASSWORD

#############################################################################
#                               TEST FUNCTIONS                              #
#############################################################################
def test_tools(client):
    response = login(client, grant_type='password', username=TEST_USERNAME, password=TEST_PASSWORD)
    at = response.get_json().get('acess_token')

    headers = {'Authorization': 'Bearer: ' + at}

    response = client.post('/config/request/upload/test_video.mp4', headers=headers)
    assert response.status_code == 200

    response = client.post('/config/request/upload/11113', headers=headers)
    assert response.status_code == 400

