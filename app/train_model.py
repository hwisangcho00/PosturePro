import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('training_data.csv') 

y = data['Form']
X = data.drop('Form', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Model Accuracy: {accuracy:.2f}')

os.makedirs('ml_model', exist_ok=True)

joblib.dump(model, 'ml_model/posture_classifier.pkl')

tree_rules = export_text(model, feature_names=list(X.columns))
print(tree_rules)