from tensorflow.python.keras.losses import SparseCategoricalCrossentropy
from keras.src.saving.legacy.model_config import model_from_json


def restore_model(path_without_extension: str):
    json_file = open(path_without_extension + ".json", 'r')
    loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path_without_extension + ".h5")
    json_file.close()
    return loaded_model


def compile_model(path_without_extension: str):
    model = restore_model(path_without_extension)
    model.compile(optimizer='adam',
                  loss=SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])
    return model
