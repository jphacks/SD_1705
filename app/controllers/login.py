from flask import Blueprint, session, render_template, request, redirect, url_for, g, flash
from models.users import UserModel
from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl

TW_KEY = 'h3gBThafXpsi9x4lC4w92NVIK'
TW_SECRET = 'Bt7C37w52zH1jLwxqYUFaRZtWHX5rK0dvi3bKWHFat6wjieUsu'

app = Blueprint('login', __name__)

twitter = OAuth1Service(
    name='twitter',
    consumer_key=TW_KEY,
    consumer_secret=TW_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    base_url='https://api.twitter.com/1.1/'
)


@app.before_request
def before_request():
    g.user = None
    if 'twitter_token' in session:
        with UserModel() as User:
            users = User.get_user_by_token(session['twitter_token'])
            g.user = []
            for user in users:
                g.user.append({
                    'id': user.twitter_id,
                    'name': user.user_name,
                    'icon': user.icon_url
                })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        oauth_callback = url_for('login.authorized', _external=True)
        params = {'oauth_callback': oauth_callback}

        r = twitter.get_raw_request_token(params=params)
        data = parse_utf8_qsl(r.content)

        session['twitter_oauth'] = (data['oauth_token'], data['oauth_token_secret'])

        return redirect(twitter.get_authorize_url(data['oauth_token'], **params))

    if 'twitter_token' in session:
        return redirect(url_for('top.top_page'))

    logining = g.user is not None
    is_login = True
    if 'is_login' in session:
        is_login = session.pop('is_login')

    return render_template('login.html', logining=logining, user=g.user, is_login=is_login)


@app.route('/logout')
def logout():
    session.pop('twitter_token', None)
    return redirect(url_for('login.login'))


@app.route('/authorized')
def authorized():
    request_token, request_token_secret = session.pop('twitter_oauth')
    if 'oauth_token' not in request.args:
        session['login_error'] = 'You did not authorize the request'
        return redirect(url_for('login.login'))
    try:
        creds = {
            'request_token': request_token,
            'request_token_secret': request_token_secret}
        params = {'oauth_verifier': request.args['oauth_verifier']}
        sess = twitter.get_auth_session(params=params, **creds)
    except Exception as e:
        session['login_error'] = 'There was a problem login into Twitter: '+str(e)
        return redirect(url_for('login.login'))

    verify = sess.get('account/verify_credentials.json',params={'format': 'json'}).json()

    with UserModel() as User:
        users_by_token = User.get_user_by_token(request_token)
        users_by_twid = User.get_user_by_twitter_id(verify['id'])
        print(users_by_token)
        print(users_by_twid)
        if users_by_token == [] and users_by_twid == []:
            users = User.create_user(verify['id'], verify['screen_name'], verify['profile_image_url'], request_token, request_token_secret)
        else:
            users = User.update_user_token(verify['id'], verify['screen_name'], request_token, request_token_secret)

        g.user = []
        for user in users:
            g.user.append({
                'id': user.twitter_id,
                'name': user.user_name,
                'icon': user.icon_url
            })
    session['twitter_token'] = request_token

    return redirect(url_for('top.top_page'))
