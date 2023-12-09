from flask import Flask

import routes
from data_restoring import restore_groups
from model_restoring import restore_model

app = Flask(__name__)
app.register_blueprint(routes.main)

app.config['SECRET_KEY'] = 'More than meets the eye'


def init():
    model_path = '../resources/models/mock_model_21022023'
    groups_path = 'datamining/idsnet07022023/groups/2cl_gr_fr_cut1pers.txt'
    class_names = ["Art & Culture personality", "Science & Technician personality"]
    model = restore_model(model_path)
    groups = restore_groups(groups_path)
    return model, groups, class_names


if __name__ == '__main__':
    MODEL, GROUPS, CLASS_NAMES = init()
    app.run()
