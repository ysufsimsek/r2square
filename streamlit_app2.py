import streamlit as st
import pandas as pd
import joblib
import webbrowser

st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.selectbox("", ["Proje Ekip Üyeleri", "Proje"])

if page == "Proje Ekip Üyeleri":
    st.title("HAKKIMIZDA")
    st.header("Proje Ekip Üyeleri")
    st.write("R2 Kare Projesinin ekip üyeleri:")
    st.write("**Yusuf ŞİMŞEK**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Mehmet AYDEMİR**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Efe Batın SEÇKİN**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("")
    st.write("Aşağıda ekip üyelerimizin GitHub ve LinkedIn hesapları bulunmaktadır")
    with st.expander("Ekip Üyeleri GitHub ve LinkedIn Bilgileri"):
        st.write("**Ekip Lideri**: Yusuf ŞİMŞEK")
        if st.button('LinkedIn - Yusuf ŞİMŞEK'):
            webbrowser.open_new_tab("https://www.linkedin.com/in/yusuf-%C5%9Fim%C5%9Fek-ab1486295/")
        if st.button('GitHub - Yusuf ŞİMŞEK'):
            webbrowser.open_new_tab("https://github.com/ysufsimsek")

        st.write("**Ekip Üyesi**: Mehmet AYDEMİR")
        if st.button('LinkedIn - Mehmet AYDEMİR'):
            webbrowser.open_new_tab("https://www.linkedin.com/in/mehmet-aydemir-7514262a5/")
        if st.button('GitHub - Mehmet AYDEMİR'):
            webbrowser.open_new_tab("https://github.com/mehmetaydemir")

        st.write("**Ekip Üyesi**: Efe Batın SEÇKİN")
        if st.button('LinkedIn - Efe Batın SEÇKİN'):
            webbrowser.open_new_tab("https://www.linkedin.com/in/efe-bat%C4%B1n-se%C3%A7kin-b78692295/")
        if st.button('GitHub - Efe Batın SEÇKİN'):
            webbrowser.open_new_tab("https://github.com/efebatinseckin")

    st.header("Proje Hakkında Bilgiler")
    st.write("Veri bilimi için programlaya giriş adlı dersimizin dönem içi proje ödevidir. 14/03/2024 tarihinde projeye başlanılmıştır. Proje belirenen bir takımın atabileceği gol sayısını tahmin etme temeli olan makine öğrenmesi projesidir.Kullanırken iyi eğleceler dileriz. ")

    st.header("Gelecek Güncellemeler")
    st.write("Daha fazla takımın gol tahminin")

elif page == "Proje":
    st.title("R2 Kare Dönem İçi Projesi")

    # Model ve scaler dosyalarının yüklendiğinden emin olun
    try:
        model = joblib.load('stacking_model.joblib')
        scaler = joblib.load('scaler.joblib')
    except Exception as e:
        st.error(f"Model veya scaler yüklenirken bir hata oluştu: {e}")
        st.stop()

    st.header("Gol Sayısı Tahmini İçin Seçilen Barcelona Maçının Gerekli İstatistiklerini Aşağıda Belirtilen Yerlere Giriniz:")
    input_data = {
        'Topla Oynama': st.number_input('Topla Oynama', min_value=0, max_value=100),
        'İsabetli Şut': st.number_input('İsabetli Şut', min_value=0, max_value=100),
        'Başarılı Paslar': st.number_input('Başarılı Paslar', min_value=0, max_value=1000),
        'Korner': st.number_input('Korner', min_value=0, max_value=100),
        'Başarılı Orta': st.number_input('Başarılı Orta', min_value=0, max_value=100)
    }

    input_df = pd.DataFrame([input_data])

    try:
        input_df_scaled = scaler.transform(input_df)
    except Exception as e:
        st.error(f"Veri ölçeklendirilirken bir hata oluştu: {e}")
        st.stop()

    if st.button('Atalıcak Golü tahmin edin'):
        try:
            prediction = model.predict(input_df_scaled)
            if input_df['İsabetli Şut'][0] == 0:
                prediction[0] = 0
            st.write(f"Tahmini Barcelonanın Atacağı Gol: {prediction[0]}")
        except Exception as e:
            st.error(f"Tahmin yapılırken bir hata oluştu: {e}")
