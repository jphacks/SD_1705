from flask import Blueprint,session,render_template,request,redirect,url_for,g,Flask
from models.users import UserModel
import json
from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl

TW_KEY = 'h3gBThafXpsi9x4lC4w92NVIK'
TW_SECRET = 'Bt7C37w52zH1jLwxqYUFaRZtWHX5rK0dvi3bKWHFat6wjieUsu'

app = Blueprint('login',__name__)

twitter = OAuth1Service(
    name='twitter',
    consumer_key=TW_KEY,
    consumer_secret=TW_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/'
)


@app.before_request
def before_request():
    g.user = None
    if 'twitter_token' in session:
        with UserModel() as User:
            g.user = User.get_user_by_token(session['twitter_token'])


@app.route('/login')
def login_main():
    return render_template('login.html')


@app.route('/user/login')
def login():
    oauth_callback = url_for('user/authorized', _external=True)
    params = {'oauth_callback':oauth_callback}

    r = twitter.get_raw_request_token(params=params)
    data = parse_utf8_qsl(r.content)

    session['twitter_oauth'] = (data['oauth_token'],data['oauth_token_secret'])

    return redirect(twitter.get_authorize_url(data['oauth_token'],**params))


@app.route('/user/logout')
def logout():
    session.pop('twitter_token',None)
    return redirect(url_for('login_main'))


@app.route('/user/authorized')
def authorized():
    request_token, request_token_secret = session.pop('twitter_oauth')
    if not 'oauth_token' in request.args:
        session['login_error'] = 'You did not authorize the request'
        return redirect(url_for('login_main'))
    try:
        creds = {
            'request_token':request_token,
            'request_token_secret':request_token_secret}
        params = {'oauth_verifier':request.args['oauth_verifier']}
        sess = twitter.get_auth_session(params=params,**creds)
    except Exception as e:
        session['login_error'] = 'There was a problem login into Twitter: '+str(e)
        return redirect(url_for('login_main'))

    verify = sess.get('account/verify_credentials.json',params={'format':'json'}).json()

    with UserModel as User:
        user = User.get_user_by_token(request_token)
        if user is None:
            User.create_user(verify['id'], verify['screen_name'], verify['profile_image_url'], request_token, request_token_secret)
        else:
            User.update_user_token(verify['id'], verify['screen_name'], request_token)

    return redirect(url_for('login_main'))
