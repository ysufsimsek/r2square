import streamlit as st
import pandas as pd
import joblib


st.title("R2 Kare Dönem İçi Projesi")


model = joblib.load('stacking_model.joblib')
scaler = joblib.load('scaler.joblib')

st.header("İstenilen İstatistikleri Giriniz")
input_data = {
    'Topla Oynama': st.number_input('Topla Oynama', min_value=0, max_value=100, value=50),
    'İsabetli Şut': st.number_input('İsabetli Şut', min_value=0, max_value=100, value=10),
    'Başarılı Paslar': st.number_input('Başarılı Paslar', min_value=0, max_value=1000, value=30),
    'Korner': st.number_input('Korner', min_value=0, max_value=100, value=5),
    'Başarılı Orta': st.number_input('Başarılı Orta', min_value=0, max_value=100, value=15)
}


input_df = pd.DataFrame([input_data])


input_df_scaled = scaler.transform(input_df)


if st.button('Tahmin Yap'):
    prediction = model.predict(input_df_scaled)
    if input_df['İsabetli Şut'][0] == 0:
        prediction[0] = 0
    st.write(f"Tahmin Sonucu: {prediction[0]}")
