from flask import Blueprint, render_template

from ..config import env

docs_routes = Blueprint('docs', __name__, url_prefix=env("URL_PREFIX","/rdm/svm-api/v1"))


@docs_routes.route('/swagger', methods=['GET'])
def swagger():
    return render_template('swaggerui.html')


@docs_routes.route('/openapi', methods=['GET'])
def openapi():
    return render_template('openapi.html')
