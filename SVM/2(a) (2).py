# -*- coding: utf-8 -*-
"""2(a)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1usyvEFLBdPeDXCc61USHygiSHykZG-aD
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# This will load our test and train dataset in a dataframe
train_file = pd.read_csv('train.csv', header=None)
test_file = pd.read_csv('test.csv', header=None)

# Extract features and labels from datasets
train_features = train_file.iloc[:, :-1].values
train_labels = train_file.iloc[:, -1].values
test_features = test_file.iloc[:, :-1].values
test_labels = test_file.iloc[:, -1].values

# As asked in the question to convert those extracted labels to {-1, 1}
train_labels = np.where(train_labels == 0, -1, 1)
test_labels = np.where(test_labels == 0, -1, 1)

# Setting up the intial parameters required
num_epochs = 100  # epoch given
penalty_values = [100 / 873, 500 / 873, 700 / 873]  # Regularization parameters
learning_rate_initial = 0.1  # Starting learning rate
rate_adjustment = 10  # Adjustment parameter for learning rate schedule

# Created Function to find the hinge loss.
def calculate_objective_value(feature_set, label_set, weights, bias_term, penalty_factor):
    margins = label_set * (np.dot(feature_set, weights) + bias_term)
    total_loss = 0.5 * np.dot(weights, weights) + penalty_factor * np.sum(np.maximum(0, 1 - margins))
    return total_loss

# Function to shuffle the training data
def randomize_data(features, labels):
    indices = np.arange(features.shape[0])
    np.random.shuffle(indices)
    return features[indices], labels[indices]

# Function created to calculate Stochastic gradient descent for SVM training
def train_svm_gradient_descent(
    feature_train, label_train, feature_test, label_test, penalty, start_rate, adjustment_param, epochs
):
    num_samples, num_attributes = feature_train.shape
    weight_vector = np.zeros(num_attributes)
    bias_value = 0
    loss_history = []

    for epoch in range(epochs):
        # This will Shuffle the training data at the start of each epoch
        feature_train, label_train = randomize_data(feature_train, label_train)

        # Formula used to calculate the current learning rate
        current_rate = start_rate / (1 + (start_rate / adjustment_param) * epoch)

        # Updating the weights and bias based on each training example
        for sample_idx in range(num_samples):
            margin_value = label_train[sample_idx] * (np.dot(weight_vector, feature_train[sample_idx]) + bias_value)
            if margin_value < 1:
                # If there are any misclassified points so handle update accordingly
                weight_vector -= current_rate * weight_vector - current_rate * penalty * label_train[sample_idx] * feature_train[sample_idx]
                bias_value += current_rate * penalty * label_train[sample_idx]
            else:
                # Incase of correctly classified points
                weight_vector -= current_rate * weight_vector

        # Calculate and store the objective value
        objective_value = calculate_objective_value(feature_train, label_train, weight_vector, bias_value, penalty)
        loss_history.append(objective_value)

    # Calculate errors on training and test sets
    train_predictions = np.sign(np.dot(feature_train, weight_vector) + bias_value)
    test_predictions = np.sign(np.dot(feature_test, weight_vector) + bias_value)
    training_error = np.mean(train_predictions != label_train)
    testing_error = np.mean(test_predictions != label_test)

    return weight_vector, bias_value, loss_history, training_error, testing_error

# Training  our SVM for each regularization parameter and plot results in the form of a graph
for penalty_factor in penalty_values:
    final_weights, final_bias, objective_history, train_error, test_error = train_svm_gradient_descent(
        train_features, train_labels, test_features, test_labels,
        penalty_factor, learning_rate_initial, rate_adjustment, num_epochs
    )

    # Noting training and test errors
    print(f"For given C = {penalty_factor:.4f}: Training Error is = {train_error:.4f}, Test Error is = {test_error:.4f}")

    # Plot the objective function curve
    plt.plot(range(num_epochs), objective_history, label=f'C = {penalty_factor:.4f}')

plt.xlabel('  E(Epochs)')
plt.ylabel('Function Value')
plt.title('Objective Function Curve for Different Regularization Parameters')
plt.legend()
plt.show()

