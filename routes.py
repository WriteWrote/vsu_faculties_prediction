from flask import Blueprint, render_template, request

from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

from data_restoring import scrape_groups_ids
from webscrapping import get_person_groups

import numpy as np


main = Blueprint("main", __name__)

MODEL = None
GROUPS = []
CLASS_NAMES = []


class CreateForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Test')


@main.route("/", methods=["POST", "GET"])
def index():
    form = CreateForm()
    if request.method == "POST":
        predictions = []
        result = ""

        person_url = form.title.data
        user_data = get_person_groups(person_url)

        if len(user_data) == 0:
            result = "Нет данных"
            predictions = [0, 0]
        else:
            clean_data_vector = [scrape_groups_ids(user_data, GROUPS)]
            predictions = MODEL.predict(clean_data_vector)
            result = CLASS_NAMES[np.argmax(predictions)]

        return render_template('result.html', title='Result', result=result, predictions=predictions,
                               classes=CLASS_NAMES, length=len(CLASS_NAMES))

    return render_template('index.html', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
