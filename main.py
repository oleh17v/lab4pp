from flask import Flask, Response
import datetime


from apischm.user import user
from apischm.authentification import authentification
from apischm.ad import advertisement

app = Flask(__name__)
app.register_blueprint(authentification)
app.register_blueprint(advertisement)
app.register_blueprint(user)

@app.route('/api/v1/hello-world-3')
def index():
    return "Hello World 3"


if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=8080)
    app.run(debug=True)
