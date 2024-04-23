import pandas as pd

file_path = 'twitter_training.csv'
data = pd.read_csv(file_path, delimiter=',', header=None, names=['ID', 'Topic', 'Sentiment', 'Text'])
print(data.head())
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
data = data.dropna()
X = data['Text']
y = data['Sentiment']
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),  
    ('classifier', LogisticRegression())  
])
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
joblib.dump(pipeline, 'best_model.pkl')
