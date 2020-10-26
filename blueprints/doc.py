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
@bp.route("/", defaults={"page": 'index.html'})
@bp.route("/<page>")
def get_doc(page: str):
    if "/" in page:
        raise NotFoundException(message='Nao encontrado')
    try:
        return render_template(page)
    except:
        raise NotFoundException(message='Nao encontrado')