# -*- coding: utf-8 -*-
"""GBM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PMXARJnV0E2WY_yh_mEtSTlWwOK_Hk0J
"""

# Importing all the important Libraries
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# Function written for pre processing data
def preprocess_data(df):
    # Replace '?' with NaN for easy handling of missing values
    df = df.replace('?', np.nan)

    # Assigning a value to a missing value using Impute Function
    imputer = SimpleImputer(strategy='most_frequent')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Conversion from categorical columns to numerical using label encoding
    categorical_columns = df.select_dtypes(include=['object']).columns
    label_encoders = {col: LabelEncoder().fit(df[col]) for col in categorical_columns}
    for column, le in label_encoders.items():
        #print("Value for column,le",column,le)
        df[column] = le.transform(df[column])

    return df

def main():
    print("Loading the data...")
    # Loading the data into a dataframe
    train_data = pd.read_csv('train_final.csv')
    #train_data.head()
    test_data = pd.read_csv('test_final.csv')
    #test_data.head()
    print("Preprocessing the data...")
    # Preprocess the data
    train_data = preprocess_data(train_data)
    test_data = preprocess_data(test_data)

    # Ensure the target column 'income>50K' is present in the training data
    if 'income>50K' not in train_data.columns:
        raise KeyError("Not Found!!")

    # Split features and target
    X_train = train_data.drop(columns='income>50K')
    y_train = train_data['income>50K']

    # Handle the test data
    if 'income>50K' in test_data.columns:
        X_test = test_data.drop(columns='income>50K')
    else:
        X_test = test_data.drop(columns='ID', errors='ignore')

    test_ids = test_data.get('ID', pd.Series(dtype='int'))

    print("Training the GBM model...")
    # Train the GBM model
    lgb_train = lgb.Dataset(X_train, label=y_train)
    #print("Train Value",lgb_train)
    params = {
        'objective': 'binary',
        'boosting_type': 'gbdt',
        'metric': 'binary_logloss',
        'learning_rate': 0.1,
        'num_leaves': 31,
        'max_depth': -1,
        'min_data_in_leaf': 20,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'seed': 0
    }

    # Training the model
    model = lgb.train(params, lgb_train, num_boost_round=100)

    # This will help in Predicting probabilities for test data
    predictions = model.predict(X_test)  # Probability of class "income>50K=1"

    print("Creating a submission file...")
    # Prepare submission with IDs starting from 1
    submission = pd.DataFrame({'ID': test_ids + 1, 'Prediction': predictions})
    submission.to_csv('Submission_lgbm.csv', index=False)
    print("Submission file 'submission_lgbm.csv' created successfully.")

if __name__ == "__main__":
    main()

