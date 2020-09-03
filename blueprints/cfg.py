from flask import Blueprint, jsonify
from utils import auth
from utils.tools import upload_component
from utils.error_handler import NotFoundException, ConflictException, BadRequestException, UnauthorizedException
#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint('cfg', __name__)

#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################

#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route('/request/upload/<string:file_name>', methods=['POST'])
def upload(file_name):
    try:
        x = file_name.split('.')
        file_extension = x[-1]
    except Exception:
        raise BadRequestException()

    #NOTE Create a new file name to avoid conflict names on S3 bucket
    new_file_name = str(uuid.uuid4())
    new_file_name = '{}.{}'.format(new_file_name, file_extension)

    upload_obj = upload_component(new_file_name)

    if not upload_obj:
        raise BadRequestException(message='Erro ao gerar componente de upload de arquivo')

    return jsonify(upload_obj)