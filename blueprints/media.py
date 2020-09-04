from flask import Blueprint, jsonify
from utils import auth
import models
from datetime import datetime
from . import video_schema, return_no_content, validate_instance
from utils.error_handler import NotFoundException, ConflictException, BadRequestException, UnauthorizedException
#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint('media', __name__)

#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################
def jsonify_video(video):
    return {
        'id': video.id,
        'name': video.name,
        'url': video.url,
        'duration': video.duration,
        'created_at': video.created_at,
        'updated_at': video.updated_at,
        'removed_at': video.removed_at,
        'removed': video.removed
    }

#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route('/', methods=['GET'])
@auth.authenticate_user
def getAll():
    page = request.args.get('page', 1)
    page_size = request.args.get('pagesize', 1000)
    all_medias = request.args.get('allmedias', 1)
    try:
        page = int(page)
        if page < 1:
            page = 1
        page_size = int(page_size)
        if page_size < 1:
            page_size = 1
        all_medias = bool(all_medias)
    except Exception:
        raise BadRequestException(message='Erro no recebimento dos parametros')

    query = models.Video.query

    if not all_medias:
        query = query.filter_by(removed=False)

    videos = query.paginate(page=page, per_page=page_size).items

    for index, video in enumerate(videos):
        videos[index] = jsonify_video(video)

    return jsonify({'medias': videos})


@bp.route('/<string:media_id>', methods=['GET'])
@auth.authenticate_user
def getOne(media_id):
    video = models.Video.query.get(media_id)
    if not video:
        raise NotFoundException(message='midia de video nao encontrada')
    response = jsonify_video(video)
    return jsonify(response)


@bp.route('/', methods=['POST'])
@auth.authenticate_admin
def insert():
    video_body = request.json
    validate_instance(payload=video_body, schema=video_schema)

    video = models.Video()
    video.name = video_body.get('name')
    video.url = video_body.get('url')
    video.duration = video_body.get('duration')

    models.db.session.add(video)
    try:
        models.db.session.commit()
        return return_no_content()
    except Exception as err:
        print(f'### Erro ao inserir midia de video: {err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')


@bp.route('/<string:media_id>', methods=['PUT'])
@auth.authenticate_admin
def update(media_id):
    video_body = request.json
    validate_instance(payload=video_body, schema=video_schema)

    video = models.Video.query.get(media_id)
    if not video or video.removed:
        raise NotFoundException(message='midia de video nao encontrada')

    video.name = video_body.get('name')
    video.url = video_body.get('url')
    video.duration = video_body.get('duration')
    video.updated_at = datetime.utcnow()

    models.db.session.add(video)
    try:
        models.db.session.commit()
        return return_no_content()
    except Exception as err:
        print(f'### Erro ao inserir midia de video: {err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')


@bp.route('/<string:media_id>', methods=['DELETE'])
@auth.authenticate_admin
def remove(media_id):
    video = models.Video.query.get(media_id)
    if not video or video.removed:
        raise NotFoundException(message='midia de video nao encontrada')

    video.removed = True
    video.removed_at = datetime.utcnow()

    models.db.session.add(video)
    try:
        models.db.session.commit()
        return return_no_content()
    except Exception as err:
        print(f'### Erro ao remover midia de video: {err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')