# src/models.py
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def train_all_models(X_train, y_train):
    """
    Trains XGBoost, Random Forest, and a Neural Network.
    Returns a dictionary of trained models.
    """
    # 1. XGBoost
    xgb = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, eval_metric="logloss")
    xgb.fit(X_train, y_train)

    # 2. Random Forest
    rf = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    rf.fit(X_train, y_train)

    # 3. Neural Network (MLP)
    nn = MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=42)
    nn.fit(X_train, y_train)

    return {
        "XGBoost": xgb,
        "RandomForest": rf,
        "NeuralNet": nn
    }