import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Generate synthetic data
np.random.seed(42)
num_samples = 1000

Vrms = np.random.normal(230, 10, num_samples)
Irms = np.random.normal(2.5, 0.5, num_samples)
Power = Vrms * Irms
kWh = np.cumsum(Power / 1000 / 360)
Cost = 5 + 8 * kWh + np.random.normal(0, 5, num_samples)

df = pd.DataFrame({
    'Vrms': Vrms,
    'Irms': Irms,
    'Power': Power,
    'kWh': kWh,
    'Cost': Cost
})

X = df[['Vrms', 'Irms', 'Power', 'kWh']]
y = df['Cost']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'ml_model/cost_predictor.pkl')
print("✅ Model trained and saved.")