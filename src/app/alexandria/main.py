from flask import Blueprint, render_template, request

blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def index():
    return render_template('index.html')