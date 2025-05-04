import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# Read the CSV file
df = pd.read_csv('DataDanhGia.csv', skipinitialspace=True)

X = df.iloc[:, 4:7].values  # Use Age_Score, Time_Score, ChuyenMon_Score
y = df.iloc[:, 7].values    # Use DanhGia (evaluation score)

# Split data into Train, Validation, and Test sets
X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.176, random_state=42)

# Build linear regression model
model = Sequential()
model.add(Dense(1, input_dim=3))  # Simple linear regression (1 output neuron)

model.summary()
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=10, validation_data=(X_val, y_val))

# Save the trained model
model.save("GiaTriChuyenNhuong.h5")
print("✅ Model has been saved to GiaTriChuyenNhuong.h5")
