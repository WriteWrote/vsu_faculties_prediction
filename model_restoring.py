from gensim.models import Word2Vec
from keras.models import model_from_json, load_model
from keras.losses import SparseCategoricalCrossentropy
from tensorflow.python.keras.losses import SparseCategoricalCrossentropy


def restore_dnn_model(path_without_extension: str):
    # loaded_model = load_model(path_without_extension, compile=True)
    json_file = open(path_without_extension + ".json", 'r')
    loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path_without_extension + ".h5")
    loaded_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    json_file.close()
    return loaded_model


def restore_word2vec_model(path: str):
    return Word2Vec.load(path)

def compile_model(path_without_extension: str):
    model = restore_dnn_model(path_without_extension)
    model.compile(optimizer='adam',
                  loss=SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])
    return model
