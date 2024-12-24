import numpy as np
import tensorflow as tf
from ml.EEG_feature_extraction import generate_feature_vectors_from_samples

already_saved = False
Emotions = {
    0: "sad",
    1: "angry",
    2: "stressed",
    3: "neutral",
    4: "relaxed",
    5: "happy",
    6: "excited",
}

emotion = 3


# Load the pre-trained LSTM model
def load_model(path="ml/best_lstm_model.keras"):
    """
    Load the pre-trained LSTM model from the given path.

    Parameters:
    path (str): The path to the pre-trained LSTM model.

    Returns:
    tf.keras.Model: The pre-trained LSTM model.
    """
    return tf.keras.models.load_model(path)


def classify_emotion(model, input_data="ml/data/test-data.csv"):
    """
    Classify the emotion based on the input data.

    Args:
    model (tf.keras.Model): The trained model to use for classification.
    input_data (numpy array or tensor): The input data to classify.
    state: Additional state information if needed.

    Returns:
    numpy array: The predicted emotion probabilities.
    """
    global already_saved
    # Generate feature vectors from the input data
    feature_vectors = generate_feature_vectors_from_samples(
        file_path=input_data, nsamples=150, period=1.0, state=1, remove_redundant=False
    )

    # Reshape the feature vectors to match the input shape expected by the model
    feature_vectors = feature_vectors.reshape(-1, 1)
    sequence_length = feature_vectors.shape[0]
    feature_vectors = feature_vectors[: sequence_length // 2548 * 2548]

    # Replace NaNs with 0 in feature_vectors
    feature_vectors = np.nan_to_num(feature_vectors, nan=0.0)
    feature_vectors = feature_vectors.reshape((-1, 2548, 1))

    # Run the classification model on the input data
    predictions = model.predict(feature_vectors)
    emotion = convert_to_emotion(predictions)
    return emotion


def convert_to_emotion(predictions):
    """
    Convert the predicted emotion probabilities to an emotion label.

    Args:
    predictions (numpy array): The predicted emotion probabilities.

    Returns:
    str: The predicted emotion label.
    """
    # Combine the negative, neutral and positive emotion probabilities to guess which Emotion is being felt
    x, y, z = predictions[0]
    print("probabilities", x, y, z)
    output = -1.5 * x + 1.5 * y + 3 * z
    output += 3
    output = round(output)
    output = int(output)
    if output < 0:
        output = 0
    elif output > 6:
        output = 6

    return Emotions[output]
