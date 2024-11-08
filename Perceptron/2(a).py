# -*- coding: utf-8 -*-
"""2(a)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rsdJ_Vank5QFcwUwqDT0mRHB3o5QgH0u
"""

import numpy as np
import pandas as pd
import math

# Here we are reading both our test and train dataset.
training_data = pd.read_csv("train.csv", header=None)
testing_data = pd.read_csv("test.csv", header=None)

# This part will help us to separate features and labels
features_train = training_data.iloc[:, :-1]
labels_train = training_data.iloc[:, -1]
features_train_aug = np.column_stack(([1] * features_train.shape[0], features_train))
features_test = testing_data.iloc[:, :-1]
features_test_aug = np.column_stack(([1] * features_test.shape[0], features_test))
labels_test = testing_data.iloc[:, -1]

# Let's set different parameters asked in the question
num_samples, num_features = features_train_aug.shape
weight_vector = np.zeros(num_features)
learning_rate = 0.001
iterations = 10
features_train_array = np.array(features_train_aug)
labels_train_array = np.array(labels_train)

# Function for prediction
def make_prediction(feature_vector, weight_vector):
    return 1 if np.dot(weight_vector.T, feature_vector) > 0 else 0

for epoch in range(iterations):
    for feature, label in zip(features_train_array, labels_train_array):
        prediction = make_prediction(feature, weight_vector)
        if prediction == 0 and label == 1:
            weight_vector += (learning_rate * feature)
        if prediction == 1 and label == 0:
            weight_vector -= (learning_rate * feature)

# This will help us in calculating the test error.
misclassification_count = 0
for feature, label in zip(features_test_aug, labels_test):
    test_prediction = make_prediction(feature, weight_vector)
    if test_prediction != label:
        misclassification_count += 1

# Final Required Output according to the questions
print("Learned weight vector is", weight_vector)
print("Average prediction error:", misclassification_count / len(features_test_aug))

