import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, recall_score
from keras.models import load_model
import numpy as np

# Load data
df = pd.read_csv('DataDanhGia.csv', skipinitialspace=True)

# Select input and output
X = df.iloc[:, 4:7].values  # Age_Score, Time_Score, ChuyenMon_Score
y = df.iloc[:, 7].values    # DanhGia

# Split data into Train, Validation, and Test sets
X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.176, random_state=42)

# Display number of samples
print(f"📊 Total samples: {len(df)}")
print(f"🧪 Train set: {len(X_train)} samples")
print(f"🔍 Validation set: {len(X_val)} samples")
print(f"🧾 Test set: {len(X_test)} samples")

# Load trained model
model = load_model("GiaTriChuyenNhuong.h5")

# Predict on test set
y_test_pred = model.predict(X_test).flatten()
y_test_pred_class = (y_test_pred >= 0.5).astype(int)

# Evaluation metrics
mae = mean_absolute_error(y_test, y_test_pred_class)
rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_class))
r2 = r2_score(y_test, y_test_pred_class)
acc = accuracy_score(y_test, y_test_pred_class)
prec = precision_score(y_test, y_test_pred_class)
rec = recall_score(y_test, y_test_pred_class)

print(f"\n📈 Mean Absolute Error (MAE): {mae:.4f}")
print(f"📉 Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"📊 R² Score: {r2:.4f}")
print(f"✅ Accuracy: {acc:.4f}")
print(f"🎯 Precision: {prec:.4f}")
print(f"🔁 Recall: {rec:.4f}")

# Predict on the first 44 test samples
X_new = X_test[:44]
y_new = y_test[:44]
y_predicted = model.predict(X_new).flatten()
y_predicted_class = (y_predicted >= 0.5).astype(int)

# Show prediction results
df_result = pd.DataFrame({
    'Actual': y_new.astype(int),
    'Predicted': y_predicted_class,
    'Score': np.round(y_predicted, 4)
})

print("\n📋 Comparison of actual vs predicted (first 20 samples):")
print(df_result.head(20))
