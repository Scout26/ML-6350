# -*- coding: utf-8 -*-
"""3(b)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uMNh5jM39i7oXFXsKWXwhSes4PM15eJJ
"""

import numpy as np
from tabulate import tabulate

# Load and prepare the dataset
def load_banknote_dataset():
    # Load training and testing data from CSV files
    train_data = np.loadtxt('/content/train.csv', delimiter=',')
    test_data = np.loadtxt('/content/test.csv', delimiter=',')

    # Separate features (inputs) and labels (outputs)
    train_inputs, train_labels = train_data[:, :-1], train_data[:, -1]
    test_inputs, test_labels = test_data[:, :-1], test_data[:, -1]

    # Standardize features to have mean 0 and standard deviation 1
    train_inputs = (train_inputs - np.mean(train_inputs, axis=0)) / np.std(train_inputs, axis=0)
    test_inputs = (test_inputs - np.mean(test_inputs, axis=0)) / np.std(test_inputs, axis=0)

    # Convert labels to binary (0 or 1)
    train_labels = (train_labels == 1).astype(int)
    test_labels = (test_labels == 1).astype(int)

    return train_inputs, train_labels, test_inputs, test_labels

# Define the sigmoid function
def sigmoid_function(value):
    return 1 / (1 + np.exp(-value))

# Calculate the loss (log-loss)
def calculate_loss(features, labels, weights):
    num_samples = len(labels)
    predictions = sigmoid_function(np.dot(features, weights))
    # Avoid log(0) errors using a small constant (1e-8)
    loss = -np.sum(labels * np.log(predictions + 1e-8) + (1 - labels) * np.log(1 - predictions + 1e-8)) / num_samples
    return loss

# Compute the gradient of the loss
def calculate_gradient(features, labels, weights):
    num_samples = len(labels)
    predictions = sigmoid_function(np.dot(features, weights))
    gradient = np.dot(features.T, (predictions - labels)) / num_samples
    return gradient

# Train the logistic regression model using SGD
def train_logistic_model(train_features, train_labels, test_features, test_labels, initial_rate, decay_factor, num_epochs):
    weights = np.zeros(train_features.shape[1])  # Initialize weights as zeros
    num_samples = len(train_labels)
    loss_table = []  # To store losses for each epoch

    for epoch in range(num_epochs):
        # Shuffle the training data
        shuffled_indices = np.random.permutation(num_samples)
        train_features, train_labels = train_features[shuffled_indices], train_labels[shuffled_indices]

        # Update weights for each training example
        for i in range(num_samples):
            learning_rate = initial_rate / (1 + (initial_rate / decay_factor) * epoch)  # Decayed learning rate
            gradient = calculate_gradient(train_features[i:i+1], train_labels[i:i+1], weights)
            weights -= learning_rate * gradient

        # Calculate training and test loss after each epoch
        train_loss = calculate_loss(train_features, train_labels, weights)
        test_loss = calculate_loss(test_features, test_labels, weights)
        loss_table.append([epoch + 1, train_loss, test_loss])

    return weights, loss_table

# Main execution block
if __name__ == "__main__":
    # Load data
    train_features, train_labels, test_features, test_labels = load_banknote_dataset()

    # Set hyperparameters
    initial_learning_rate = 0.1  # Starting learning rate
    decay_rate = 0.01            # Rate at which learning rate decreases
    total_epochs = 100           # Total number of epochs to train

    # Train the model
    final_weights, epoch_losses = train_logistic_model(train_features, train_labels, test_features, test_labels,
                                                       initial_learning_rate, decay_rate, total_epochs)

    # Calculate accuracy
    train_predictions = sigmoid_function(np.dot(train_features, final_weights)) >= 0.5
    test_predictions = sigmoid_function(np.dot(test_features, final_weights)) >= 0.5
    train_accuracy = np.mean(train_predictions == train_labels) * 100
    test_accuracy = np.mean(test_predictions == test_labels) * 100

    # Display the results in a table
    print("Progress by Epoch(1,2,3,....100):")
    print(tabulate(epoch_losses, headers=["Epoch", "Training Error", "Test Error"], floatfmt=".6f"))

    # Final accuracy results
    print("\nFinal Results:")
    print(f"Training Accuracy: {train_accuracy:.2f}%")
    print(f"Testing Accuracy: {test_accuracy:.2f}%")

