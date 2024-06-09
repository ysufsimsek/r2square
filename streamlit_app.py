import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.metrics import mean_squared_error, f1_score
import joblib


file_path = 'veri.xlsx'
data = pd.read_excel(file_path)


features = ["Topla Oynama", "İsabetli Şut", "Başarılı Paslar", "Korner", "Başarılı Orta"]
X = data[features]
y = data['Ev Gol']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


best_svr = SVR(C=0.1, gamma='auto', kernel='rbf')
rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
xgb_model = XGBRegressor(n_estimators=200, random_state=42)


stacking_model = StackingRegressor(
    estimators=[
        ('svr', best_svr),
        ('rf', rf_model),
        ('xgb', xgb_model)
    ],
    final_estimator=RandomForestRegressor(n_estimators=100, random_state=42)
)
stacking_model.fit(X_train_scaled, y_train)


joblib.dump(stacking_model, 'stacking_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model ve scaler başarıyla kaydedildi.")

print()