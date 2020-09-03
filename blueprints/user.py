from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
import models
from . import user_schema_insert, user_schema_update, change_pass_schema, validate_instance, return_no_content
from utils.error_handler import BadRequestException, ConflictException, NotFoundException, ForbiddenException
from utils import auth

#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint('user', __name__)


#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################
def jsonify_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'active': user.active,
        'admin': user.admin,
        'created_at': user.created_at,
        'removed_at': user.removed_at,
        'updated_at': user.updated_at,
        'removed': user.removed
    }


#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route('/', methods=["GET"])
@auth.authenticate_admin
def getAll():
    page = request.args.get('page', 1)
    page_size = request.args.get('pagesize', 1000)
    try:
        page = int(page)
        if page < 1:
            page = 1
        page_size = int(page_size)
        if page_size < 1:
            page_size = 1
    except Exception:
        raise BadRequestException(message='Erro no recebimento dos parametros de paginacao')
    users = models.User.query.paginate(page=page, per_page=page_size).items
    for index, user in enumerate(users):
        users[index] = jsonify_user(user)
    return jsonify({'users': users})


@bp.route('/', methods=["POST"])
@auth.authenticate_admin
def insert():
    user_body = request.json
    validate_instance(payload=user_body, schema=user_schema_insert)
    password = user_body.get('password')
    user = models.User()
    user.username = user_body.get('username')
    user.name = user_body.get('name')
    user.password = models.User.hash_password(password)
    models.db.session.add(user)
    try:
        models.db.session.commit()
        return return_no_content()
    except Exception as err:
        print(f'Erro ao inserir usuario: {err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')


@bp.route('/<string:user_id>', methods=["GET"])
@auth.authenticate_admin
def getOne(user_id):
    user = models.User.query.get(user_id)
    if not user or user.removed:
        raise NotFoundException(message='usuario nao encontrado')
    response = jsonify_user(user)
    return jsonify(response)


@bp.route('/<string:user_id>', methods=["PUT"])
@auth.authenticate_admin
def update(user_id):
    user_body = request.json
    validate_instance(payload=user_body, schema=user_schema_update)
    user = models.User.query.get(user_id)
    if not user or user.removed or not user.active:
        raise NotFoundException(message='usuario nao encontrado')

    user.username = user_body.get('username')
    user.name = user_body.get('name')
    user.updated_at = datetime.utcnow()

    models.db.session.add(user)
    try:
        models.db.session.commit()
        return return_no_content()
    except Exception as err:
        print(f'Erro ao atualizar usuario: {err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')


@bp.route('/<string:user_id>', methods=["DELETE"])
@auth.authenticate_admin
def remove(user_id):
    user = models.User.query.get(user_id)
    if not user or user.removed:
        raise NotFoundException(message='Usuario nao encontrado')
    user.removed = True
    user.removed_at = datetime.utcnow()
    models.db.session.add(user)
    try:
        models.db.session.commit()
    except Exception as err:
        print(f'Erro ao remover usuario{err}')
        models.db.session.rollback()
        raise ConflictException(message='Conflito no banco de dados')
    return return_no_content()


@bp.route('/change/password', methods=['POST'])
@auth.authenticate_user
def change_pass():
    payload = request.get_json()

    validate_instance(payload=payload, schema=change_pass_schema)

    current_password = payload.get('current_password')
    new_password = payload.get('new_password')

    user = auth.get_user()

    if current_password == new_password:
        raise ConflictException(message='Senhas informadas iguais')

    if user.password != models.User.hash_password(current_password):
        raise ConflictException(message='Informacoes invalidas')

    user.password = models.User.hash_password(new_password)

    models.db.session.add(user)

    models.db.session.commit()

    return return_no_content()