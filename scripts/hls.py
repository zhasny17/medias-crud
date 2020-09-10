import requests
import os
import secrets
import random
import mysql.connector
from datetime import datetime
import shutil
import boto3


#############################################################################
#                                 VARIABLES                                 #
#############################################################################
s3_client = boto3.client('s3')

DATABASE_INFO = {
    'user': os.environ.get('DB_USERNAME'),
    'database': os.environ.get('DB_NAME'),
    'host': os.environ.get('DB_HOST'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': os.environ.get('DB_PORT')
}

HLS_BUCKET_NAME = os.environ.get('HLS_BUCKET_NAME')


#############################################################################
#                             FUNCTIONS                                     #
#############################################################################
def main(id: str):
    # TODO Retrive download url from database based on video ID
    download_url = 'url'

    while not os.path.exists(f'videos/{id}'):
        os.makedirs(f'videos/{id}')

    with requests.get(download_url, allow_redirects=True) as r:
        with open(f'videos/{id}/video.mp4', 'wb') as video_file:
            # NOTE Prevent loading the entire response in the memory, only 25kb at a time
            for piece in r.iter_content(chunk_size=25000):
                if piece:
                    video_file.write(piece)

    # NOTE Generate 16bytes key to encript videos
    asciiBin = os.urandom(16)
    with open(f'videos/{id}/enc.key', 'wb') as r:
        r.write(asciiBin)

    # NOTE Generate IV to encript videos (hexadecimal of 16 bytes)
    iv = str(secrets.token_hex(16))

    # NOTE Generate and write the keyinfo file
    with open(f'videos/{id}/enc.keyinfo', 'w') as r:
        r.write(f'/videos/{id}/enc.key\nvideos/{id}/enc.key\n{iv}')

    os.system(f'ffmpeg -y -i videos/{id}/video.mp4 -hls_time 9 -hls_key_info_file videos/{id}/enc.keyinfo -hls_playlist_type vod -hls_segment_filename "videos/{id}/fileSequence%d.ts" videos/{id}/prog_index.m3u8'.format(id=id))

    # NOTE Save info on database
    # try:
    #     date = datetime.utcnow()
    #     connection = mysql.connector.connect(**DATABASE_INFO)
    #     insert_sql = """INSERT INTO hls_videos (video_id, `key`, iv, created_at, removed) VALUES (%s, %s, %s, %s, %s)"""
    #     cursor = connection.cursor()
    #     insert_tuple = (id, asciiBin, iv, str(date), False)
    #     result = cursor.execute(insert_sql, insert_tuple)
    #     connection.commit()
    #     cursor.close()
    # except mysql.connector.Error as error:
    #     print(f'@@@@@@@@@@ Erro ao inserir video: {str(error)}')

    # NOTE Remove video file before upload hls files to S3
    os.remove('videos/{id}/video.mp4')
    print('>>>>>>>>>>>> arquivo de video removido do diretorio')

    # NOTE Copy folder on local path to s3
    for root, dirs, files in os.walk("videos/"):
        for name in files:
            dir_path = root + name
            response = s3_client.upload_file(dir_path, bucket_name, dir_path)
    print('>>>>>>>>>>>> Arquivos transferiados para a S3')

    shutil.rmtree(f'videos/{id}')


if __name__ == '__main__':
    # main(id='123')
