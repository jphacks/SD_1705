from flask import Flask
from controllers import search_result, top

app = Flask(__name__)

# ここにアプリを追加していく
apps = [
    search_result.app,
    top.app
]

for a in apps:
    app.register_blueprint(a)


if __name__ == '__main__':
    app.run()
