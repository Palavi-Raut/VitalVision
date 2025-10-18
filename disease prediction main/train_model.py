import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression

# ✅ Load Datasets (Ensure the correct path)
diabetes_dataset = pd.read_csv(r"C:\Users\dell\VitalVision\disease prediction main\data\diabetes.csv")
heart_data = pd.read_csv(r"C:\Users\dell\VitalVision\disease prediction main\data\heart_dataset.csv")

# ✅ Preprocess Diabetes Data
X_diabetes = diabetes_dataset.drop(columns="Outcome", axis=1)
Y_diabetes = diabetes_dataset["Outcome"]

scaler_diabetes = StandardScaler()
X_diabetes = scaler_diabetes.fit_transform(X_diabetes)

X_train_diabetes, X_test_diabetes, Y_train_diabetes, Y_test_diabetes = train_test_split(
    X_diabetes, Y_diabetes, test_size=0.2, stratify=Y_diabetes, random_state=2
)

classifier_diabetes = svm.SVC(kernel="linear")
classifier_diabetes.fit(X_train_diabetes, Y_train_diabetes)

# ✅ Preprocess Heart Disease Data
X_heart = heart_data.drop(columns="target", axis=1)
Y_heart = heart_data["target"]

X_train_heart, X_test_heart, Y_train_heart, Y_test_heart = train_test_split(
    X_heart, Y_heart, test_size=0.2, stratify=Y_heart, random_state=2
)

model_heart = LogisticRegression(max_iter=1000)
model_heart.fit(X_train_heart, Y_train_heart)

#  Save the models
pickle.dump(classifier_diabetes, open("diabetes_model.pkl", "wb"))
pickle.dump(scaler_diabetes, open("diabetes_scaler.pkl", "wb"))
pickle.dump(model_heart, open("heart_model.pkl", "wb"))

print("✅ Models trained and saved successfully!")
