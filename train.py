import numpy as np
import pandas
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder

def get_bin(x, n=0):
    """
    Get the binary representation of x.

    Parameters
    ----------
    x : int
    n : int
        Minimum number of digits. If x needs less digits in binary, the rest
        is filled with zeros.

    Returns
    -------
    str
    """
    return format(x, 'b').zfill(n)

def calculate_label(X):
  ch = ['ie', 'sn', 'tf', 'jp']
  y = []

  for x in X:
    sp = np.array_split(x, 4)
    i = 0
    tmp = ""

    for c in sp:
      tmp += ch[i][0] if np.sum(c) > 2 else  ch[i][1]
      i += 1
    y.append(tmp)

  return np.array(y)


def generate_patterns():
  patterns = []
  for i in reversed(range(0, 2 ** 5)): # 32 (permutasi untuk 1 kategori (I/E))
    patterns.append([int(i) for i in get_bin(i, 5)])

  return np.array(patterns)


def generate_dataset():
  arr = generate_patterns()

  X = []

  for i in range(0, 2 ** 3): # only need 8, no need 16... duplicate.. leverage symetry
    flp = get_bin(i, 4)

    temp = []
    i = 0

    # check we need flip or not
    for f in flp:
      if f == '0':
        temp.append(arr)
      else:
        xf = np.flip(arr, 0)
        temp.append(xf)
      i += 1
    
    x = np.concatenate(temp, axis=1)
    X.append(x)
  
  X = np.vstack(X)
  y = calculate_label(X)

  X = np.tile(X, (4, 1))
  y = np.tile(np.array(y), 4)

  return (X, y)

def create_model():
    model = keras.Sequential()
    model.add(layers.Dense(50, input_dim=20, activation='relu'))
    model.add(layers.Dense(50, activation='relu'))
    model.add(layers.Dense(16, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X, dummy_y, epochs=200)
    return model


if __name__ == "__main__":
    X, y = generate_dataset()

    mbti_class = ['istj', 'enfp', 'istp', 'enfj', 'isfj', 'entp', 'isfp', 'entj', 'intj', 'esfp', 'intp', 'esfj', 'infj', 'estp', 'infp', 'estj']

    encoded_Y = [mbti_class.index(x) for x in y]
    
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = tf.keras.utils.to_categorical(encoded_Y)

    model = create_model()
    model.fit(X, dummy_y, epochs=200)
    model.save('model/')

    _, accuracy = model.evaluate(X, dummy_y)
    print('Accuracy: %.2f' % (accuracy*100))

    