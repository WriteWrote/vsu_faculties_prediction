from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from keras.saving.legacy.model_config import model_from_json

main = Blueprint("main", __name__)

CLASS_NAMES = ["Art & Culture personality", "Science & Technician personality"]

GROUPS_PATH = 'datamining/idsnet07022023/groups/2cl_gr_fr_cut1pers.txt'

MOCK_MODEL_H5 = 'datamining/idsnet07022023/mockmodel/mock_model_21022023.h5'
MOCK_MODEL_JSON = 'datamining/idsnet07022023/mockmodel/mock_model_21022023.json'


def restore_model():
    # json_file = open('trainingmodels//perseptron//probability_model.json', 'r')
    json_file = open(MOCK_MODEL_JSON, 'r')

    loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    # loaded_model.load_weights("trainingmodels//perseptron//probability_model.h5")
    loaded_model.load_weights(MOCK_MODEL_H5)

    json_file.close()

    return loaded_model


def restore_groups():
    lines = []
    with open(GROUPS_PATH, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    file.close()
    return lines


GROUPS_LIST = restore_groups()


def scrape_groups_ids(full_data):
    clean_groups = []

    for group in full_data:
        clean_groups.append(str(group[0]))

    result = []

    for group in GROUPS_LIST:
        if clean_groups.__contains__(group):
            result.append(1)
        else:
            result.append(0)
    # result[529] = 1
    return result


class CreateForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Test')


# @main.route("/index")
@main.route("/", methods=["POST", "GET"])
def index():
    form = CreateForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        person_url = form.title.data

        # person_url = "https://vk.com/captainofwardrobe"
        # person_url = "https://vk.com/id219869843"
        # person_url = "https://vk.com/raf057"

        model = restore_model()
        # GROUPS_LIST = restore_groups()
        # model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        model.compile(optimizer='adam',
                      loss=tensorflow.keras.losses.SparseCategoricalCrossentropy(),
                      metrics=['accuracy'])

        user_data = get_person_groups(person_url)

        clean_data_vector = []
        clean_data_vector.append(scrape_groups_ids(user_data))
        # clean_data_vector[0].insert(0, 0)

        if clean_data_vector[0].__contains__(1):
            print("yes")

        vector = pandas.DataFrame(clean_data_vector)

        predictions = []
        result = ""

        if len(user_data) == 0:
            result = "Нет данных"
            predictions = [0, 0]
        else:
            predictions = model.predict(clean_data_vector)
            result = CLASS_NAMES[np.argmax(predictions)]

        return render_template('result.html', title='Result', result=result, predictions=predictions,
                               classes=CLASS_NAMES, length=len(CLASS_NAMES))

    return render_template('index.html', form=form)


# return "main page here"


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/result", methods=["POST", "GET"])
def result(result):
    return render_template('result.html', title='Result', result=result)
