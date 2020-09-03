from flask import Blueprint, render_template
from utils.error_handler import NotFoundException

#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint("doc", __name__)

#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################


#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route("/", methods=['GET'])
def doc(page: str):
    try:
        return render_template('index.html')
    except:
        raise NotFoundException()