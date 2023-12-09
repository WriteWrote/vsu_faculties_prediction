import numpy
from flask import Blueprint, render_template, request

from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

from data_restoring import scrape_groups_ids, read_lines
from model_restoring import restore_model
from webscrapping import get_person_groups

import numpy as np

main = Blueprint("main", __name__)


def init():
    model_path = 'resources/models/mock_model_21022023'
    groups_path = 'resources/data/2cl_gr_fr_cut1pers.txt'
    class_names_path = 'resources/data/class_names.txt'

    model = restore_model(model_path)
    groups = read_lines(groups_path)
    class_names = read_lines(class_names_path)

    return model, groups, class_names


class CreateForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Test')


MODEL, GROUPS, CLASS_NAMES = init()


@main.route("/", methods=["POST", "GET"])
def index():
    form = CreateForm()
    if request.method == "POST":
        predictions = []
        result_ = ""

        person_url = form.title.data
        user_data = get_person_groups(person_url)

        if len(user_data) == 0:
            result_ = "Нет данных"
            predictions = [0, 0]
        else:
            clean_data_vector = numpy.array([scrape_groups_ids(user_data, GROUPS)])
            predictions = MODEL.predict(clean_data_vector)
            result_ = CLASS_NAMES[np.argmax(predictions)]

        return render_template('result.html', title='Result', result=result_, predictions=predictions,
                               classes=CLASS_NAMES, length=len(CLASS_NAMES))

    return render_template('index.html', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/result", methods=["POST", "GET"])
def result(result_):
    return render_template('result.html', title='Result', result=result_)
