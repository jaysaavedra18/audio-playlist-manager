# ruff: noqa

import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


# Define a list of feature columns
feature_columns = [
    # Librosa features
    "mfcc",
    "chroma_cens",
    "chroma_cqt",
    "chroma_stft",
    "tonnetz",
    "spectral_contrast",
    "spectral_centroid",
    "spectral_bandwidth",
    "spectral_rolloff",
    "rmse",
    "zcr",
    # EchoNest features
    # "acousticness",
    # "danceability",
    # "energy",
    # "instrumentalness",
    # "liveness",
    # "speechiness",
    # "tempo",
    # "valence",
]


# Define a function for preprocessing data
def preprocess_data(X_train, X_test, y_train, y_test, reduce_features=False):
    # Shuffle training data
    X_train, y_train = shuffle(X_train, y_train, random_state=42)

    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    # Standardize features
    scaler = StandardScaler(copy=False)
    scaler.fit_transform(X_train)
    scaler.transform(X_test)

    if reduce_features:
        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=0.99)  # Keep 99% of variance
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)

        # Use Lasso for feature selection
        lasso = Lasso(alpha=0.001)
        lasso.fit(X_train, y_train_encoded)
        mask = lasso.coef_ != 0
        X_train = X_train[:, mask]
        X_test = X_test[:, mask]

        print(f"Selected {mask.sum()} features after Lasso feature selection.")

    return X_train, X_test, y_train_encoded, y_test_encoded


# Define a function to initialize the classifier
def get_classifier(model_classifier="SVM"):
    if model_classifier == "RF":
        return RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_classifier == "GPM":
        return XGBClassifier(
            n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42, n_jobs=-1
        )
    elif model_classifier == "NN":
        return MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation="relu",
            max_iter=200,
            random_state=42,
        )
    elif model_classifier == "SVM":
        return SVC()
    else:
        raise ValueError(
            "Invalid model_classifier. Choose from 'RF', 'GPM', 'NN', 'SVM'."
        )


# Define a function to train and evaluate the model
def train_and_evaluate(
    X_train, X_test, y_train_encoded, y_test_encoded, model_classifier="SVM"
):
    clf = get_classifier(model_classifier)
    clf.fit(X_train, y_train_encoded)
    score = clf.score(X_test, y_test_encoded)
    print(f"Accuracy: {score:.2%}")
    return clf, score
