import streamlit as st
import pandas as pd
import joblib
import pickle
import numpy as np
import requests
from io import BytesIO

# GitHub'dan dosyayı indir
def download_file_from_github(url):
    response = requests.get(url)
    response.raise_for_status()  # Hata varsa tetikler
    return BytesIO(response.content)

# GitHub'dan pkl dosyasını indir
url = 'https://github.com/kullanici_adi/depo_adi/raw/main/dosya.pkl'  # GitHub dosya URL'si
file_content = download_file_from_github(url)

# pkl dosyasını yükle
model = pickle.load(file_content)

# Kullanıcıdan giriş verisi alalım
st.header("İstenilen İstatistikleri Giriniz")
input_data = {
    'Topla Oynama': st.number_input('Topla Oynama', min_value=0, max_value=100, value=50),
    'İsabetli Şut': st.number_input('İsabetli Şut', min_value=0, max_value=100, value=10),
    'Başarılı Paslar': st.number_input('Başarılı Paslar', min_value=0, max_value=1000, value=30),
    'Korner': st.number_input('Korner', min_value=0, max_value=100, value=5),
    'Başarılı Orta': st.number_input('Başarılı Orta', min_value=0, max_value=100, value=15)
}

# Girdi verisini DataFrame'e dönüştürelim
input_df = pd.DataFrame([input_data])

# Veriyi standartlaştıralım
input_df_scaled = scaler.transform(input_df)

# Tahmin yapalım
if st.button('Tahmin Yap'):
    prediction = model.predict(input_df_scaled)
    if input_df['İsabetli Şut'][0] == 0:
        prediction[0] = 0
    st.write(f"Tahmin Sonucu: {prediction[0]}")

# Sayfanın sonuna açıklama ekleyelim
st.text("Bu uygulama Streamlit kullanılarak oluşturulmuştur.")
