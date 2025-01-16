# -*- coding: utf-8 -*-
"""Fruits_Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TLmrwUfqKyauWCKjtTjWtxolsqCVb4zz
"""

!mkdir data

cd data

# downloading the data store
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/apple.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/banana.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/blueberry.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/grapes.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/pear.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/pineapple.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/watermelon.npy

cd ..

# importing libraries
from sklearn.model_selection import train_test_split as tts
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.utils import to_categorical
from random import randint
import numpy as np
import os
from PIL import Image

N_FRUITS = 7
FRUITS = ['apple', 'banana', 'blueberry', 'grapes', 'pear', 'pineapple', 'watermelon']

N = 5000

N_EPOCHS = 10

files = ["apple.npy", "banana.npy", "blueberry.npy", "grapes.npy", "pear.npy", "pineapple.npy", "watermelon.npy"]

# helper functions
def load(dir, reshaped, files):

  data = []
  for file in files:
    f = np.load(dir + file)
    if reshaped:
      new_f = []
      for i in range(len(f)):
        x = np.reshape(f[i], (28, 28))
        x = np.expand_dims(x, axis=0)
        x = np.reshape(f[i], (28, 28, 1))
        new_f.append(x)
      f = new_f
    data.append(f)
  return data

def normalize(data):
  return np.interp(data, [0, 255], [-1, 1])

def denormalize(data):
  return np.interp(data, [-1, 1], [0, 255])

def visualize(array):
  array = np.reshape(array, (28, 28))
  img = Image.fromarray(array)
  return img

def set_limit(arrays, n):
  new = []
  for array in arrays:
    i = 0
    for item in array:
      if i == n:
        break
      new.append(item)
      i += 1
  return new

def make_labels(N1, N2):
  labels = []
  for i in range(N1):
    labels += [i] * N2
  return labels

# apple_fruit = load("data/", False, ['apple.npy'])

# visualize(apple_fruit[0][0])

fruits = load("data/", True, files)
fruits = set_limit(fruits, N)
fruits = list(map(normalize, fruits))
labels = make_labels(N_FRUITS, N)
x_train, x_test, y_train, y_test = tts(fruits, labels, test_size=0.05)

Y_train = to_categorical(y_train, N_FRUITS)
Y_test = to_categorical(y_test, N_FRUITS)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(N_FRUITS, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(np.array(x_train), np.array(Y_train), batch_size=32, epochs=N_EPOCHS)

print("Training complete")

print("Evaluating model")

preds = model.predict(np.array(x_test))

score = 0
for i in range(len(preds)):
  if np.argmax(preds[i]) == y_test[i]:
    score += 1

print("Accuracy:", ((score + 0.0) / len(preds)) * 100)

model.save("fruits"+".h5")

print("Model saved")