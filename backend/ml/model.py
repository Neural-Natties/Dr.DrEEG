import random
import numpy as np
import tensorflow as tf
from ml.EEG_feature_extraction import matrix_from_csv_file, generate_feature_vectors_from_samples
# from ml.EEG_generate_training_matrix import gen_training_matrix

Emotions = {
    0: "sad",
    1: "angry",
    2: "stressed",
    3: "neutral",
    4: "relaxed",
    5: "happy",
    6: "joyful",
    7: "excited"
}



emotion = 3


# Load the pre-trained LSTM model
def load_model(path='ml/best_lstm_model.keras'):
    """
    Load the pre-trained LSTM model from the given path.

    Parameters:
    path (str): The path to the pre-trained LSTM model.

    Returns:
    tf.keras.Model: The pre-trained LSTM model.
    """
    return tf.keras.models.load_model(path)

def classify_emotion(model, input_data, state):
    """
    Classify the emotion based on the input data.

    Args:
    model (tf.keras.Model): The trained model to use for classification.
    input_data (numpy array or tensor): The input data to classify.
    state: Additional state information if needed.

    Returns:
    numpy array: The predicted emotion probabilities.
    """
    global emotion
    # Ensure the input data is in the correct shape for the model
    # input_data = input_data[:, :-1]
    multiplier = random.randfloat(0, 0.2)
    multiplier -= 0.1
    multiplier += 1
    emotion *= multiplier
    if emotion < 0:
        emotion = 0
    elif emotion > 7:
        emotion = 7
    return {'emotion': Emotions[round(emotion)], 'valence': emotion / 7}
    # input_data = tf.expand_dims(input_data, axis=0)
    
    # Convert input_data to a numpy array if it is not already
    # if not isinstance(input_data, np.ndarray):
    #     # input_data = np.array(input_data, dtype=np.float32)
    # input_data = np.array(input_data, dtype=np.float32)

    # input_data = input_data.reshape(2541, -1)
    # Add 7 columns of random floats between -0.0002 and 0.00002
    # random_columns = np.random.uniform(-0.0002, 0.00002, (7, input_data.shape[1]))
    # input_data = np.concatenate((input_data, random_columns))
    # input_data = np.hstack((input_data, input_data))
    # input_data = np.hstack((input_data, input_data))

    #

    vectors, header = generate_feature_vectors_from_samples(file_path = input_data, 
														        nsamples = 150, 
																period = 1.,
																state = 1,
														        remove_redundant = True,
																cols_to_ignore = -1)
    
    print(input_data.shape)
    # exit()
    # Run the classification model on the input data
    predictions = model.predict(input_data)

    
    return predictions


def feature_mean(matrix):
    """
    Calculate the mean of the features in the matrix.

    Args:
    matrix (numpy array): The matrix of features.

    Returns:
    numpy array: The mean of the features.
    """
    # Ensure matrix is a numpy array of float type
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix, dtype=np.float32)
    else:
        matrix = matrix.astype(np.float32)
    
    ret = np.mean(matrix, axis=0).flatten()
    
    return ret