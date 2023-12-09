from flask import Blueprint, render_template, request, redirect, url_for

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from app import GROUPS_PATH, CLASS_NAMES, MODEL
from data_restoring import scrape_groups_ids, restore_groups
from webscrapping import get_person_groups

import numpy as np

main = Blueprint("main", __name__)


class CreateForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Test')


@main.route("/", methods=["POST", "GET"])
def index():
    form = CreateForm()
    if request.method == "POST":
        person_url = form.title.data

        user_data = get_person_groups(person_url)

        clean_data_vector = []
        clean_data_vector.append(scrape_groups_ids(user_data, restore_groups(GROUPS_PATH)))

        if clean_data_vector[0].__contains__(1):
            print("yes")

        predictions = []
        result = ""

        if len(user_data) == 0:
            result = "Нет данных"
            predictions = [0, 0]
        else:
            predictions = MODEL.predict(clean_data_vector)
            result = CLASS_NAMES[np.argmax(predictions)]

        return render_template('result.html', title='Result', result=result, predictions=predictions,
                               classes=CLASS_NAMES, length=len(CLASS_NAMES))

    return render_template('index.html', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/result", methods=["POST", "GET"])
def result(result):
    return render_template('result.html', title='Result', result=result)
