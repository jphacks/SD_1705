from flask import Blueprint, render_template, session

app = Blueprint('top', __name__)


@app.route('/top', methods=['GET'])
def top_page():
    error = None
    if session.get('search_error') is not None:
        error = session['search_error']
        session.pop('search_error', None)

    return render_template(
        'top.html',
        error=error
    )