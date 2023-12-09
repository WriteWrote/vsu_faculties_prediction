from flask import Flask
import routes

app = Flask(__name__)
app.register_blueprint(routes.main)
app.config['SECRET_KEY'] = 'More than meets the eye'

if __name__ == '__main__':
    app.run()
