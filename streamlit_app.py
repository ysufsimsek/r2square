import streamlit as st
import pandas as pd
import joblib
import requests

# GitHub'dan joblib dosyalarını indirmek için yardımcı fonksiyon
def download_file(url, local_filename):
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)

# GitHub'daki dosyaların URL'leri
model_url = 'https://github.com/ysufsimsek/r2square/raw/main/.devcontainer/stacking_model.pkl'
scaler_url = 'https://github.com/ysufsimsek/r2square/raw/main/.devcontainer/scaler.pkl'

# Dosyaları yerel olarak indir
model_file = 'stacking_model.pkl'
scaler_file = 'scaler.pkl'
download_file(model_url, model_file)
download_file(scaler_url, scaler_file)

st.title("R2 Kare Dönem İçi Projesi")

# Model ve scaler dosyalarını yükle
model = joblib.load(model_file)
scaler = joblib.load(scaler_file)

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
