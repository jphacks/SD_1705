from flask import Flask
from controllers import my_page

app = Flask(__name__)

# ここにアプリを追加していく
apps = [
    my_page.app
]

for a in apps:
    app.register_blueprint(a)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
