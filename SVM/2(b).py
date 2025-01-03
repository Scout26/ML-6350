# -*- coding: utf-8 -*-
"""2(b)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WekV151pqOlSekuOL5EK5IUOc_15ULnr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load training and testing datasets into a Dtaframe
train_data = pd.read_csv('train.csv', header=None)
test_data = pd.read_csv('test.csv', header=None)

# Extract features and labels
features_train = train_data.iloc[:, :-1].values
labels_train = train_data.iloc[:, -1].values
features_test = test_data.iloc[:, :-1].values
labels_test = test_data.iloc[:, -1].values

# Convert labels to {-1, 1} according to the question
labels_train = np.where(labels_train == 0, -1, 1)
labels_test = np.where(labels_test == 0, -1, 1)

# Initialize required parameters
max_epochs = 100  # epochs
regularization_params = [100 / 873, 500 / 873, 700 / 873]  # Regularization values (C)
initial_learning_rate = 0.1  # Starting learning rate

# Function to compute hinge loss objective
def compute_hinge_loss(features, labels, weights, bias, reg_param):
    margins = labels * (np.dot(features, weights) + bias)
    hinge_losses = np.maximum(0, 1 - margins)
    loss = 0.5 * np.dot(weights, weights) + reg_param * np.sum(hinge_losses)
    return loss

# Function to shuffle the data
def shuffle_data(features, labels):
    indices = np.arange(features.shape[0])
    np.random.shuffle(indices)
    return features[indices], labels[indices]

# SVM training with SGD
def svm_train_sgd(
    train_features, train_labels, test_features, test_labels, reg_param, initial_rate, epochs
):
    num_samples, num_features = train_features.shape
    weights = np.zeros(num_features)
    bias = 0
    loss_history = []

    for epoch in range(epochs):
        # Shuffle the training data at the start of each epoch
        train_features, train_labels = shuffle_data(train_features, train_labels)

        # Calculate the Learning rate
        current_rate = initial_rate / (1 + epoch)

        for i in range(num_samples):
            margin = train_labels[i] * (np.dot(weights, train_features[i]) + bias)
            if margin < 1:
                # Check and Update for misclassified points
                weights -= current_rate * weights - current_rate * reg_param * train_labels[i] * train_features[i]
                bias += current_rate * reg_param * train_labels[i]
            else:
                # Similiarly Update for correctly classified points
                weights -= current_rate * weights

        # Compute and store the hinge loss after each epoch
        epoch_loss = compute_hinge_loss(train_features, train_labels, weights, bias, reg_param)
        loss_history.append(epoch_loss)

    # Calculate training and test errors
    train_predictions = np.sign(np.dot(train_features, weights) + bias)
    test_predictions = np.sign(np.dot(test_features, weights) + bias)
    train_error = np.mean(train_predictions != train_labels)
    test_error = np.mean(test_predictions != test_labels)

    return weights, bias, loss_history, train_error, test_error

# Train our SVM for each regularization parameter and visualize the results
for reg_param in regularization_params:
    w_final, b_final, loss_values, error_train, error_test = svm_train_sgd(
        features_train, labels_train, features_test, labels_test, reg_param, initial_learning_rate, max_epochs
    )

    # Print the output
    print(f"For C = {reg_param:.4f}: Training Error is = {error_train:.4f}, Test Error is = {error_test:.4f}")

    # Plot the hinge loss curve
    plt.plot(range(max_epochs), loss_values, label=f'C = {reg_param:.4f}')

plt.xlabel('E(Epochs)')
plt.ylabel('Function Value')
plt.title('Hinge Loss Curve for Different C Value')
plt.legend()
plt.grid()
plt.show()

