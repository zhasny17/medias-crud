from flask import Blueprint
from utils import auth
from utils.tools import upload_component
from utils.error_handler import NotFoundException, ConflictException, BadRequestException, UnauthorizedException
#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint('login', __name__)

#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################

#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route('/request/upload/<string:file_name>', methods=['POST'])
def upload(file_name):
    upload_obj = upload_component(file_name)

    if not upload_obj:
        raise BadRequestException(message='Erro ao gerar componente de upload de arquivo')

    return jsonify(upload_obj)