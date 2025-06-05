import string

import nltk
import numpy
from flask import Blueprint, render_template, request
from nltk import SnowballStemmer

from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

import data_restoring
from data_restoring import process_group_names, read_lines
from model_restoring import restore_dnn_model, restore_word2vec_model
from webscrapping import get_person_groups

import spacy
from spacy.cli import download

# download("ru_core_news_sm")
import ru_core_news_sm
nlp = spacy.load("ru_core_news_sm")

main = Blueprint("main", __name__)


def init():
    # nltk.download(["stopwords", "punkt", "wordnet", "omw-1.4"])
    stopwords_ = nltk.corpus.stopwords.words("russian")
    stopwords_.extend(nltk.corpus.stopwords.words("english"))
    data_restoring.stopwords = stopwords_
    data_restoring.stoppunkt = string.punctuation + "\"s...—«»|\'``•()"
    data_restoring.nlp = ru_core_news_sm.load()
    data_restoring.stemmer = SnowballStemmer(language='russian')

    predicting_model_path = 'resources/models/2025_04_26_model_4cl_acc65'
    word2vec_model_path = 'resources/models/2025_04_23_students_moscow_voronezh_word2vec.model'
    class_names_path = 'resources/data/class_names.txt'

    predicting_model = restore_dnn_model(predicting_model_path)
    word2vec_model = restore_word2vec_model(word2vec_model_path)
    class_names = read_lines(class_names_path)

    return predicting_model, word2vec_model, class_names


class CreateForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Test')


DNN_MODEL, WORD2VEC_MODEL, CLASS_NAMES = init()


@main.route("/", methods=["POST", "GET"])
def index():
    form = CreateForm()
    if request.method == "POST":

        person_url = form.title.data
        user_data = get_person_groups(person_url)

        if len(user_data) == 0:
            result_ = "Невозможно получить данные"
            predictions = [0, 0, 0, 0]
        else:
            clean_data_vector = numpy.array([process_group_names(user_data, WORD2VEC_MODEL)])
            predictions = DNN_MODEL.predict(clean_data_vector)
            predictions = numpy.round(predictions, 3)
            result_ = CLASS_NAMES[numpy.argmax(predictions)]

        return render_template('result.html',
                               title='Result',
                               result=result_,
                               predictions=predictions,
                               classes=CLASS_NAMES,
                               length=len(CLASS_NAMES))

    return render_template('index.html', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/result", methods=["POST", "GET"])
def result(result_):
    return render_template('result.html', title='Result', result=result_)
