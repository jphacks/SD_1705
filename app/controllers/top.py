from flask import Blueprint, render_template, session, redirect, url_for

app = Blueprint('top', __name__)


@app.route('/top', methods=['GET'])
def top_page():
    error = None
    # ユーザID求める
    if session.get('twitter_token') is None:
        session['is_login'] = False
        return redirect(url_for('login.login'))

    if session.get('search_error') is not None:
        error = session['search_error']
        session.pop('search_error', None)

    return render_template(
        'top.html',
        error=error
    )