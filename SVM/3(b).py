# -*- coding: utf-8 -*-
"""3(b)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MxC4ql04OHIhz6XttamoTHJUspO93Wud
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.spatial.distance import cdist

# Load training and testing datasets into a dataframe
training_data = pd.read_csv('train.csv', header=None)
testing_data = pd.read_csv('test.csv', header=None)

# Separate features and labels for both datasets
X_train = training_data.iloc[:, :-1].values
y_train = training_data.iloc[:, -1].values
X_test = testing_data.iloc[:, :-1].values
y_test = testing_data.iloc[:, -1].values

# Transform label to 1 and -1
y_train = np.where(y_train == 0, -1, 1)
y_test = np.where(y_test == 0, -1, 1)

# Define values for hyperparameters
regularization_values = [100 / 873, 500 / 873, 700 / 873]  # Different C values
kernel_gamma_values = [0.1, 0.5, 1, 5, 100]  # Gamma values for RBF kernel

# Function to compute RBF kernel matrix
def compute_rbf_kernel(data1, data2, gamma):
    # Compute squared Euclidean distances and apply Gaussian kernel formula
    squared_dists = cdist(data1, data2, 'sqeuclidean')
    return np.exp(-squared_dists / gamma)

# Objective function for dual optimization in SVM
def svm_dual_objective(alpha, kernel_matrix, labels):
    # Maximize the dual objective function
    return 0.5 * alpha @ (labels * labels.T * kernel_matrix) @ alpha - np.sum(alpha)

# Create a zero
def zero_sum_constraint(alpha, labels):
    return np.dot(alpha, labels)

# Training SVM using RBF kernel for different combinations of C and gamma
for gamma in kernel_gamma_values:
    # Precompute kernel matrix using RBF
    kernel_matrix = compute_rbf_kernel(X_train, X_train, gamma)

    for C in regularization_values:
        num_samples = X_train.shape[0]

        # Initialize alpha to zero
        initial_alpha = np.zeros(num_samples)

        # Define constraints and bounds for optimization
        constraints = ({'type': 'eq', 'fun': zero_sum_constraint, 'args': (y_train,)})
        bounds = [(0, C) for _ in range(num_samples)]

        # Perform optimization using SLSQP
        result = minimize(
            svm_dual_objective, initial_alpha,
            args=(kernel_matrix, y_train),
            method='SLSQP', bounds=bounds, constraints=constraints
        )

        # Extract optimized alpha values
        optimized_alpha = result.x

        # Calculate the bias term using support vectors
        support_vector_indices = np.where((optimized_alpha > 1e-5) & (optimized_alpha < C - 1e-5))[0]
        if len(support_vector_indices) > 0:
            bias = np.mean(
                y_train[support_vector_indices] -
                np.dot(kernel_matrix[support_vector_indices], (optimized_alpha * y_train))
            )
        else:
            bias = 0

        # Print bias for the current combination of C and gamma
        print(f"For value of C = {C:.4f}, Gamma value = {gamma}: Bias = {bias:.4f}")

        # Calculate prediction errors on the training dataset
        train_predictions = np.sign(np.dot(kernel_matrix, (optimized_alpha * y_train)) + bias)
        train_error = np.mean(train_predictions != y_train)

        # Calculate prediction errors on the test dataset
        test_kernel_matrix = compute_rbf_kernel(X_test, X_train, gamma)
        test_predictions = np.sign(np.dot(test_kernel_matrix, (optimized_alpha * y_train)) + bias)
        test_error = np.mean(test_predictions != y_test)

        # Print training and test errors
        print(f"For value of C = {C:.4f}, Gamma = {gamma}: Training Error is = {train_error:.4f}, Test Error is = {test_error:.4f}")

