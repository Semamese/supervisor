from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump
import pandas as pd


if __name__ == '__main__':
    data = pd.read_csv('right.csv',index_col=0)
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        LogisticRegression(max_iter=10000)
    )

    model.fit(X_train, y_train)
    dump(model, 'right_clicker_prediction.joblib')
    y_pred = model.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))