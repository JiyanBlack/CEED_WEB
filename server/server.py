from flask import Flask, url_for, send_from_directory
import pandas

app = Flask(__name__, static_url_path='')

# Routes


@app.route('/web/')
def root():
    return app.send_static_file('Web/static/index.html')


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return send_from_directory('Web/static', path)


@app.route('/cardid/<int:id>/', methods=['GET'])
def get_user_json(id):
    return str(id)


if __name__ == "__main__":
    app.run()
