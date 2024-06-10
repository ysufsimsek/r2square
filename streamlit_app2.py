import streamlit as st
import pandas as pd
import joblib

st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.selectbox("", ["Proje Ekip Üyeleri", "Proje"])

if page == "Proje Ekip Üyeleri":
    st.title("Proje Ekip Üyeleri")
    st.write("R2 Kare Projesinin ekip üyeleri:")
    st.write("**Yusuf ŞİMŞEK**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Mehmet AYDEMİR**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Efe Batın SEÇKİN**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("")
    st.write("Aşağıda ekip üyelerimizin GitHub ve LinkedIn hesapları bulunmaktadır")
    with st.expander("Ekip Üyeleri GitHub ve LinkedIn Bilgileri"):
        st.write("**Ekip Lideri**: Yusuf ŞİMŞEK")
        st.markdown('<a href="https://www.linkedin.com/in/yusuf-%C5%9Fim%C5%9Fek-ab1486295/" target="_blank"><button>LinkedIn - Yusuf ŞİMŞEK</button></a>', unsafe_allow_html=True)
        st.markdown('<a href="https://github.com/ysufsimsek" target="_blank"><button>GitHub - Yusuf ŞİMŞEK</button></a>', unsafe_allow_html=True)

        st.write("**Ekip Üyesi**: Mehmet AYDEMİR")
        st.markdown('<a href="https://www.linkedin.com/in/mehmet-aydemir-7514262a5/" target="_blank"><button>LinkedIn - Mehmet AYDEMİR</button></a>', unsafe_allow_html=True)
        st.markdown('<a href="https://github.com/mehmetaydemir" target="_blank"><button>GitHub - Mehmet AYDEMİR</button></a>', unsafe_allow_html=True)

        st.write("**Ekip Üyesi**: Efe Batın SEÇKİN")
        st.markdown('<a href="https://www.linkedin.com/in/efe-bat%C4%B1n-se%C3%A7kin-b78692295/" target="_blank"><button>LinkedIn - Efe Batın SEÇKİN</button></a>', unsafe_allow_html=True)
        st.markdown('<a href="https://github.com/EfeSeckinn" target="_blank"><button>GitHub - Efe Batın SEÇKİN</button></a>', unsafe_allow_html=True)

elif page == "Proje":
    st.title("R2 Kare Dönem İçi Projesi")

    # Model ve scaler dosyalarının yüklendiğinden emin olun
    try:
        model = joblib.load('stacking_model.pkl')
        scaler = joblib.load('scaler.pkl')
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

    if st.button('Atılacak Golü tahmin edin'):
        try:
            prediction = model.predict(input_df_scaled)
            if input_df['İsabetli Şut'][0] == 0:
                prediction[0] = 0
            st.write(f"Tahmini Barcelona'nın Atacağı Gol: {prediction[0]}")
        except Exception as e:
            st.error(f"Tahmin yapılırken bir hata oluştu: {e}")
