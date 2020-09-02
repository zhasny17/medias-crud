import boto3
import os
from urllib.parse import urljoin

#############################################################################
#                                 VARIABLES                                 #
#############################################################################
s3_client = boto3.client('s3')

UPLOAD_BUCKET_NAME = os.environ.get('UPLOAD_BUCKET_NAME')
UPLOAD_URL_EXPIRATION = os.environ.get('UPLOAD_URL_EXPIRATION')
UPLOAD_BUCKET_ENDPOINT = os.environ.get('UPLOAD_BUCKET_ENDPOINT')


#############################################################################
#                                  FUNCTIONS                                #
#############################################################################

def upload_component(fileName):
    if not fileName:
        return None
    try:
        upload_object = s3_client.generate_presigned_post(Bucket=UPLOAD_BUCKET_NAME, Key=fileName, ExpiresIn=int(UPLOAD_URL_EXPIRATION))
        image_url = urljoin(UPLOAD_BUCKET_ENDPOINT, fileName)
    except Exception as err:
        return None
    return {
        'uploadObject': upload_object,
        'file_url': image_url
    }
