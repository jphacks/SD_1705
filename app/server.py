from flask import Flask, redirect, url_for
from controllers import my_page, search_result, login, top, fav

SECRET_KEY = '\xa2Q\x97\x85\x9f\xbc\x92\x1a\xdf\x85\xbe\xc1\xea{\x97\xb4|\xe83\x1b\xd0x\xca'

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ここにアプリを追加していく
apps = [
    my_page.app,
    search_result.app,
    login.app,
    search_result.app,
    top.app,
    fav.app
]

for a in apps:
    app.register_blueprint(a)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login.login'))


if __name__ == '__main__':
    app.run()
