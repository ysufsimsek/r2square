import streamlit as st
import pandas as pd
import joblib
import webbrowser
import numpy as np
import matplotlib.pyplot as plt

yillar = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


def temizle_ve_isle(df_istatistik, df_maclar):
    df_istatistik.drop(["Köşe Vuruşu", "Ofsaytlar", "Direkten Dönen", "Fauller"], axis=1, inplace=True)
    df_istatistik.dropna(inplace=True)
    df_maclar.dropna(inplace=True)

    df_istatistik["Pas Başarı(%)"] = df_istatistik["Pas Başarı(%)"].str.replace('%', '').astype(float)
    df_istatistik["Topla Oynama"] = df_istatistik["Topla Oynama"].str.replace('%', '').astype(float)

    df_istatistik[['Başarılı Orta', "Toplam Orta"]] = df_istatistik['Orta'].str.split('/', expand=True)
    df_istatistik['Başarılı Orta'] = pd.to_numeric(df_istatistik['Başarılı Orta'])
    df_istatistik['Toplam Orta'] = pd.to_numeric(df_istatistik['Toplam Orta'])
    df_istatistik.drop(["Orta"], axis=1, inplace=True)

    df_maclar[["Ev Gol", "Deplasman Gol"]] = df_maclar["skor"].str.split("-", expand=True)
    df_maclar['Ev Gol'] = pd.to_numeric(df_maclar['Ev Gol'])
    df_maclar['Deplasman Gol'] = pd.to_numeric(df_maclar['Deplasman Gol'])

    return df_istatistik, df_maclar


def ortalamalari_hesapla(df_istatistik):
    stats = np.array(df_istatistik.mean())
    stats_name = np.array(df_istatistik.columns)
    return pd.DataFrame(stats, index=stats_name)


def hesapla_sezon_sonuclar(df_maclar):
    sezon_sonuclar = df_maclar["sonuc"].value_counts()
    win = sezon_sonuclar.get("G", 0)
    draw = sezon_sonuclar.get("B", 0)
    lose = sezon_sonuclar.get("M", 0)
    mbp = ((win * 3) + draw) / (win + draw + lose)
    return win, draw, lose, mbp


# Yıllık verilerin okunması ve işlenmesi
yillar_str = ["14", "15", "16", "17", "18", "19", "20", "21", "22"]
avareage_stats = {}
sezon_sonuclar = {}
mbp_values = []

for yil in yillar_str:
    df_istatistik = pd.read_excel(f"istatistikler_{yil}.xlsx")
    df_maclar = pd.read_excel(f"maclar_{yil}.xlsx")
    df_istatistik, df_maclar = temizle_ve_isle(df_istatistik, df_maclar)
    avareage_stats[yil] = ortalamalari_hesapla(df_istatistik)
    sezon_sonuclar[yil] = hesapla_sezon_sonuclar(df_maclar)
    mbp_values.append(sezon_sonuclar[yil][3])
    print(avareage_stats[yil])
    print(
        f"Sezon {yil} - Kazanma: {sezon_sonuclar[yil][0]}, Beraberlik: {sezon_sonuclar[yil][1]}, Mağlubiyet: {sezon_sonuclar[yil][2]}, Maç Başı Puan: {sezon_sonuclar[yil][3]}")

ortalamalar = {}

for yil in yillar_str:
    ortalamalar[yil] = {
        "ort_sut": avareage_stats[yil].loc["Toplam Şut"].values[0],
        "ort_toplaOynama": avareage_stats[yil].loc["Topla Oynama"].values[0],
        "ort_pasIsabeti": avareage_stats[yil].loc["Pas Başarı(%)"].values[0],
        "ort_korner": avareage_stats[yil].loc["Korner"].values[0],
        "basarili_orta_ort": avareage_stats[yil].loc["Başarılı Orta"].values[0]
    }

print(ortalamalar)


st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.selectbox("", ["Hakkımızda", "Proje","Grafik"])

if page == "Hakkımızda":
    st.title("HAKKIMIZDA")
    st.header("R2 Kare Projesinin ekip üyeleri")
    st.write("**Yusuf ŞİMŞEK**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Mehmet AYDEMİR**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("**Efe Batın SEÇKİN**: Fırat Üniversitesi Yapay Zeka ve Veri Mühendisliği 1.sınıf öğrencisi")
    st.write("")
    st.write("Aşağıda ekip üyelerimizin GitHub ve LinkedIn hesapları bulunmaktadır")
    with st.expander("Ekip Üyeleri GitHub ve LinkedIn Bilgileri"):
        st.write("**Ekip Lideri**: Yusuf ŞİMŞEK")
        st.markdown(
            '<a href="https://www.linkedin.com/in/yusuf-%C5%9Fim%C5%9Fek-ab1486295/" target="_blank"><button>LinkedIn - Yusuf ŞİMŞEK</button></a>',
            unsafe_allow_html=True)
        st.markdown(
            '<a href="https://github.com/ysufsimsek" target="_blank"><button>GitHub - Yusuf ŞİMŞEK</button></a>',
            unsafe_allow_html=True)

        st.write("**Ekip Üyesi**: Mehmet AYDEMİR")
        st.markdown(
            '<a href="https://www.linkedin.com/in/mehmet-aydemir-7514262a5/" target="_blank"><button>LinkedIn - Mehmet AYDEMİR</button></a>',
            unsafe_allow_html=True)
        st.markdown(
            '<a href="https://github.com/mehmetaydemr-8" target="_blank"><button>GitHub - Mehmet AYDEMİR</button></a>',
            unsafe_allow_html=True)

        st.write("**Ekip Üyesi**: Efe Batın SEÇKİN")
        st.markdown(
            '<a href="https://www.linkedin.com/in/efe-bat%C4%B1n-se%C3%A7kin-b78692295/" target="_blank"><button>LinkedIn - Efe Batın SEÇKİN</button></a>',
            unsafe_allow_html=True)
        st.markdown(
            '<a href="https://github.com/EfeSeckinn" target="_blank"><button>GitHub - Efe Batın SEÇKİN</button></a>',
            unsafe_allow_html=True)
    st.header("Proje Hakkında Bilgiler")
    st.write(
        "Veri bilimi için programlaya giriş adlı dersimizin dönem içi proje ödevidir. 14/03/2024 tarihinde projeye başlanılmıştır. Proje belirenen bir takımın atabileceği gol sayısını tahmin etme temeli olan makine öğrenmesi projesidir.Kullanırken iyi eğleceler dileriz. ")

    st.header("Gelecek Güncellemeler")
    st.write("-Proje sayfasına lig seçme butonu")
    st.write("-Proje sayfasına seçilen ligden takım seçme butonu")
    st.write("-Daha fazla veri kullanan makine öğrenmesi")

    st.header("Güncelleme geçmişi")
    st.write("Güncelleme geçmişi bulunmamaktadır")

elif page == "Proje":
    st.title("R2 Kare Dönem İçi Projesi")

    # Model ve scaler dosyalarının yüklendiğinden emin olun
    try:
        model = joblib.load('stacking_model.joblib')
        scaler = joblib.load('scaler.joblib')
    except Exception as e:
        st.error(f"Model veya scaler yüklenirken bir hata oluştu: {e}")
        st.stop()

    st.header(
        "Gol Sayısı Tahmini İçin Seçilen Barcelona Maçının Gerekli İstatistiklerini Aşağıda Belirtilen Yerlere Giriniz:")
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
            st.write(f"Tahmini Barcelonanın Atacağı Gol: {prediction[0]}")
        except Exception as e:
            st.error(f"Tahmin yapılırken bir hata oluştu: {e}")

elif page == "Grafik":
    yil_menusu = st.selectbox("Bir yıl seçin:",
                              ["Yıllara Göre Ortalama Topla Oynama Grafiği",
                               "Yıllara Göre Ortalama Şut Grafiği",
                               "Yıllara göre pas isabeti grafiği",
                               "Yıllara göre ortalama korner grafiği",
                               "Yıllara göre başarılı orta grafiği",
                               "Ortalama şut-Ortalam başarılı orta grafiği",
                               "Yıllara Göre Maç Başı Puan Grafiği"])

    # Grafiklerin oluşturulması
    ort_pasIsabeti = [ortalamalar[yil]["ort_pasIsabeti"] for yil in yillar_str]
    ort_toplaOynama = [ortalamalar[yil]["ort_toplaOynama"] for yil in yillar_str]
    ort_sut = [ortalamalar[yil]["ort_sut"] for yil in yillar_str]
    ort_korner = [ortalamalar[yil]["ort_korner"] for yil in yillar_str]
    basarili_orta_ort = [ortalamalar[yil]["basarili_orta_ort"] for yil in yillar_str]

    if yil_menusu == "Yıllara Göre Ortalama Topla Oynama Grafiği":
        plt.plot(yillar, ort_toplaOynama, "r-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Ortalama Topla Oynama")
        plt.title("Yıllara Göre Ortalama Topla Oynama Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Yıllara Göre Ortalama Şut Grafiği":
        plt.plot(yillar, ort_sut, "b-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Ortalama Şut")
        plt.title("Yıllara Göre Ortalama Şut Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Yıllara göre pas isabeti grafiği":
        plt.plot(yillar, ort_pasIsabeti, "g-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Ortalama Pas İsabeti")
        plt.title("Yıllara Göre Ortalama Pas İsabeti Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Yıllara göre ortalama korner grafiği":
        plt.plot(yillar, ort_korner, "y-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Ortalama Korner")
        plt.title("Yıllara Göre Ortalama Korner Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Yıllara göre başarılı orta grafiği":
        plt.plot(yillar, basarili_orta_ort, "m-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Ortalama Başarılı Orta")
        plt.title("Yıllara Göre Ortalama Başarılı Orta Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Ortalama şut-Ortalam başarılı orta grafiği":
        plt.plot(ort_sut, basarili_orta_ort, "c-*")
        plt.xlabel("Ortalama Şut")
        plt.ylabel("Ortalama Başarılı Orta")
        plt.title("Ortalama Şut - Ortalama Başarılı Orta Grafiği")
        st.pyplot(plt)

    elif yil_menusu == "Yıllara Göre Maç Başı Puan Grafiği":
        plt.plot(yillar, mbp_values, "g-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Maç Başı Puan")
        plt.title("Yıllara Göre Maç Başı Puan Grafiği")
        st.pyplot(plt)
