import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

if __name__ == "__main__":
    mbti_class = ['istj', 'enfp', 'istp', 'enfj', 'isfj', 'entp', 'isfp', 'entj', 'intj', 'esfp', 'intp', 'esfj', 'infj', 'estp', 'infp', 'estj']

    model = keras.models.load_model('model')
    test_input = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    result = model.predict(np.array( [test_input,] ))
    mbti = np.argmax(result, axis=-1)
    print(mbti_class[mbti[0]])