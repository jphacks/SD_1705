from flask import Blueprint

app = Blueprint('login',__name__)


@app.before_request
def before_request():
    pass


@app.route('/login')
def main():
    pass


@app.route('/user/login')
def login():
    pass


@app.route('/user/logout')
def logout():
    pass


@app.route('/user/authorized')
def authorized():
    pass