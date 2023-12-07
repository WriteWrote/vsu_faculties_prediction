from flask import Flask

app = Flask(__name__)

app = Flask(__name__)
app.register_blueprint(routes.main)

app.config['SECRET_KEY'] = 'More than meets the eye'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
