from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/api/v1/hello-world-3')
def index():
    return "Hello World 3"


if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=8080)
    app.run(debug=True)
