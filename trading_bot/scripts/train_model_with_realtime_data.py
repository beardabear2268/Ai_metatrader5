import pandas as pd
import numpy as np
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# Load and preprocess the data
def load_data(file_path):
    """
    Load data from a CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully from {}".format(file_path))
        return df
    except FileNotFoundError as e:
        logging.error("File not found: {}. Error: {}".format(file_path, e))
        return pd.DataFrame()

def preprocess_data(df):
    """
    Preprocess the data for training.
    """
    df = df.dropna()
    df['mid'] = (df['ask'] + df['bid']) / 2
    df['price_change'] = df['close'].shift(-1) - df['close']
    df['label'] = (df['price_change'] > 0).astype(int)
    df = df.drop(columns=['time', 'price_change'])

    return df.drop(columns=['label']), df['label']

def train_model(X, y):
    """
    Train the model using Random Forest classifier.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    param_grid = {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_features': ['sqrt', 'log2'],
        'classifier__max_depth': [4, 5, 6, 7, 8]
    }

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    
    train_accuracy = accuracy_score(y_train, best_model.predict(X_train))
    test_accuracy = accuracy_score(y_test, best_model.predict(X_test))
    
    logging.info("Training Accuracy: {:.2f}".format(train_accuracy))
    logging.info("Test Accuracy: {:.2f}".format(test_accuracy))

    return best_model

def save_model(model, file_name):
    """
    Save the trained model to a file.
    """
    joblib.dump(model, file_name)
    logging.info("Model saved to {}".format(file_name))

def main():
    logging.basicConfig(filename='../logs/train_model_with_realtime_data.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    data_file = '../data/EURUSD_2_hours_data.csv'
    data = load_data(data_file)

    if data.empty:
        logging.error("No data loaded. Exiting.")
        return
    
    X, y = preprocess_data(data)
    model = train_model(X, y)
    save_model(model, '../models/trained_realtime_model.pkl')

if __name__ == "__main__":
    main()