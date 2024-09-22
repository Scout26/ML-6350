# -*- coding: utf-8 -*-
"""ML Assignment Solution 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YHWB433b2qoGmsMDSjMtoeeHYRCat5mP
"""

# Import Important Libraries for data manipulation
import pandas as pd
import math
import csv
from collections import Counter
#Loading data in Dataframe
train = pd.read_csv('train.csv', header=None)
test = pd.read_csv('test.csv', header=None)

# Assigning column names to the given dataset.
column = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']
train.columns = column
test.columns = column

display(train.head())
display(test.head())
class Node:
    def __init__(self, attribute=None, label=None, branches=None):
        self.attribute = attribute
        self.label = label
        self.branches = branches or {}

def load_data(filename):
    with open(filename, 'r') as f:
        return [line.strip().split(',') for line in f]

def entropy(labels):
    counts = Counter(labels)
    total = sum(counts.values())
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def majority_error(labels):
    counts = Counter(labels)
    majority = max(counts.values())
    total = sum(counts.values())
    return (total - majority) / total

def gini_index(labels):
    counts = Counter(labels)
    total = sum(counts.values())
    return 1 - sum((count / total) ** 2 for count in counts.values())

def information_gain(data, attribute_index, labels, criterion):
    attribute_values = [example[attribute_index] for example in data]
    total_score = criterion(labels)

    weighted_score = 0
    for value in set(attribute_values):
        subset_labels = [labels[i] for i in range(len(data)) if attribute_values[i] == value]
        weight = len(subset_labels) / len(labels)
        weighted_score += weight * criterion(subset_labels)

    return total_score - weighted_score
# Main ID3 Algorithm Function Starts here
def id3(data, attributes, labels, criterion, max_depth=float('inf')):
    if len(set(labels)) == 1:
        return Node(label=labels[0])

    if not attributes or max_depth == 0:
        return Node(label=Counter(labels).most_common(1)[0][0])

    best_attribute = max(attributes, key=lambda attr: information_gain(data, attr, labels, criterion))

    node = Node(attribute=best_attribute)

    for value in set(example[best_attribute] for example in data):
        subset_data = [example for example in data if example[best_attribute] == value]
        subset_labels = [labels[i] for i in range(len(data)) if data[i][best_attribute] == value]

        if not subset_data:
            node.branches[value] = Node(label=Counter(labels).most_common(1)[0][0])
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_attribute]
            node.branches[value] = id3(subset_data, remaining_attributes, subset_labels, criterion, max_depth - 1)

    return node

def predict(tree, example):
    if tree.label is not None:
        return tree.label

    attribute_value = example[tree.attribute]
    if attribute_value in tree.branches:
        return predict(tree.branches[attribute_value], example)
    else:
        # If attribute value not seen during training, return most common label
        return max(tree.branches.values(), key=lambda node: node.label if node.label else '')

def evaluate(tree, data):
    correct = sum(1 for example in data if predict(tree, example) == example[-1])
    return correct / len(data)

# Load data after assigning columns
train_data = load_data('train.csv')
test_data = load_data('test.csv')

# Separate features and labels
train_features = [example[:-1] for example in train_data]
train_labels = [example[-1] for example in train_data]
test_features = [example[:-1] for example in test_data]
test_labels = [example[-1] for example in test_data]

# Define attributes
attributes = list(range(len(train_features[0])))

# Define criteria
criteria = {
    'Information Gain': entropy,
    'Majority Error': majority_error,
    'Gini Index': gini_index
}

results = []
depth_of_tree = int(input("Enter the depth of the tree: "))
for depth in range(1, depth_of_tree+1):
    for criterion_name, criterion_func in criteria.items():
        tree = id3(train_features, attributes, train_labels, criterion_func, max_depth=depth)

        train_accuracy = evaluate(tree, train_data)
        test_accuracy = evaluate(tree, test_data)

        results.append({
            'depth': depth,
            'criterion': criterion_name.lower().replace(' ', '_'),
            'train_error': 1 - train_accuracy,
            'test_error': 1 - test_accuracy
        })

# Convert results to DataFrame and format
df = pd.DataFrame(results)
df['train_error'] = df['train_error'].round(3)
df['test_error'] = df['test_error'].round(6)

# Sort the DataFrame
df = df.sort_values(['depth', 'criterion'])

# Reset index and display
df = df.reset_index(drop=True)
display(df)
