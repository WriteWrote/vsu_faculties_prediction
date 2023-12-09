from flask import Flask

import routes
from model_restoring import restore_model

app = Flask(__name__)
app.register_blueprint(routes.main)

app.config['SECRET_KEY'] = 'More than meets the eye'

MODEL_PATH = '../resources/models/mock_model_21022023'
GROUPS_PATH = 'datamining/idsnet07022023/groups/2cl_gr_fr_cut1pers.txt'
CLASS_NAMES = ["Art & Culture personality", "Science & Technician personality"]
MODEL = restore_model(MODEL_PATH)

if __name__ == '__main__':
    app.run()
