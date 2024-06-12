import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Sayfa ayarları
st.set_page_config(page_title="R2 Kare Projesi")

# CSS stili ile sayfa arka planını ve sidebar stilini ayarlama
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(#1e3c72, #2a5298);
        color: white;
    }
    .sidebar .sidebar-content h2 {
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #1e3c72;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2a5298;
    }
    .st-expander {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True
)

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

def hesapla_mac_basina_atilan_gol(df_maclar):
    atilan_gol = df_maclar['Ev Gol'] + df_maclar['Deplasman Gol']
    toplam_gol = atilan_gol.sum()
    mac_sayisi = len(atilan_gol)
    mac_basina_gol = toplam_gol / mac_sayisi
    return mac_basina_gol

# Yıllık verilerin okunması ve işlenmesi
yillar_str = ["14", "15", "16", "17", "18", "19", "20", "21", "22"]
avareage_stats = {}
sezon_sonuclar = {}
mbp_values = []
mac_basina_atilan_gol_values = []

for yil in yillar_str:
    df_istatistik = pd.read_excel(f"istatistikler_{yil}.xlsx")
    df_maclar = pd.read_excel(f"maclar_{yil}.xlsx")
    df_istatistik, df_maclar = temizle_ve_isle(df_istatistik, df_maclar)
    avareage_stats[yil] = ortalamalari_hesapla(df_istatistik)
    sezon_sonuclar[yil] = hesapla_sezon_sonuclar(df_maclar)
    mbp_values.append(sezon_sonuclar[yil][3])
    mac_basina_atilan_gol_values.append(hesapla_mac_basina_atilan_gol(df_maclar))
    print(avareage_stats[yil])
    print(f"Sezon {yil} - Kazanma: {sezon_sonuclar[yil][0]}, Beraberlik: {sezon_sonuclar[yil][1]}, Mağlubiyet: {sezon_sonuclar[yil][2]}, Maç Başı Puan: {sezon_sonuclar[yil][3]}")

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
page = st.sidebar.selectbox("", ["Ana Sayfa","Hakkımızda", "Proje", "Grafik"])

if page == "Ana Sayfa":
    st.title("Hoş Geldiniz!")
    st.write("""
        Bu proje kapsamında, belirlenen bir takımın maç sonuçlarına dair istatistikler ve analizler yapabilirsiniz. Ayrıca,
        maç başına gol tahmini gibi makine öğrenmesi modellerini de deneyebilirsiniz.
    """)
    st.subheader("Proje Özellikleri:")
    st.write("""
        - **İstatistik Analizi:** Belirli sezonlara ait maç istatistiklerini görüntüleyin ve analiz edin.
        - **Maç Tahmini:** Makine öğrenmesi modeli kullanarak bir takımın maç başına atacağı gol sayısını tahmin edin.
        - **Grafikler:** Sezon bazında çeşitli istatistiksel grafikler oluşturun ve analiz edin.
    """)

    # Bilgilendirme kartları
    st.markdown(
        """
        <div style="display: flex; gap: 20px;">
            <div style="background: #1e3c72; padding: 20px; border-radius: 10px; flex: 1; color: white;">
                <h3>İstatistik Analizi</h3>
                <p>Sezonlara ait maç istatistiklerini analiz edin ve takım performansını değerlendirin.</p>
            </div>
            <div style="background: #2a5298; padding: 20px; border-radius: 10px; flex: 1; color: white;">
                <h3>Maç Tahmini</h3>
                <p>Makine öğrenmesi modeli ile takımın maç başına atacağı gol sayısını tahmin edin.</p>
            </div>
            <div style="background: #1e3c72; padding: 20px; border-radius: 10px; flex: 1; color: white;">
                <h3>Grafikler</h3>
                <p>Farklı sezonlara ait çeşitli istatistiksel grafikler oluşturun ve analiz edin.</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    st.header("Proje Hakkında Bilgiler")
    st.write(
        "Veri bilimi için programlamaya giriş adlı dersimizin dönem içi proje ödevidir. 14/03/2024 tarihinde projeye başlanılmıştır. Proje belirlenen bir takımın atabileceği gol sayısını tahmin etme temeli olan makine öğrenmesi projesidir. Kullanırken iyi eğlenceler dileriz.")

    st.header("Gelecek Güncellemeler")
    st.write("- Proje sayfasına lig seçme butonu")
    st.write("- Proje sayfasına seçilen ligden takım seçme butonu")
    st.write("- Daha fazla veri kullanan makine öğrenmesi")

elif page == "Hakkımızda":
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
            '<a href="https://github.com/mehmetaydemir" target="_blank"><button>GitHub - Mehmet AYDEMİR</button></a>',
            unsafe_allow_html=True)

        st.write("**Ekip Üyesi**: Efe Batın SEÇKİN")
        st.markdown(
            '<a href="https://www.linkedin.com/in/efe-bat%C4%B1n-se%C3%A7kin-b78692295/" target="_blank"><button>LinkedIn - Efe Batın SEÇKİN</button></a>',
            unsafe_allow_html=True)
        st.markdown(
            '<a href="https://github.com/efebatinseckin" target="_blank"><button>GitHub - Efe Batın SEÇKİN</button></a>',
            unsafe_allow_html=True)
   
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
    yil_menusu = st.selectbox("Görüntülemek İstediğiniz Grafiği Seçiniz:",
                              ["Yıllara Göre Ortalama Topla Oynama Grafiği",
                               "Yıllara Göre Ortalama Şut Grafiği",
                               "Yıllara göre pas isabeti grafiği",
                               "Yıllara göre ortalama korner grafiği",
                               "Yıllara göre başarılı orta grafiği",
                               "Ortalama şut-Ortalam başarılı orta grafiği",
                               "Yıllara Göre Maç Başı Puan Grafiği",
                               "Yıllara Göre Maç Başına Atılan Gol Grafiği"])

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

    elif yil_menusu == "Yıllara Göre Maç Başına Atılan Gol Grafiği":
        plt.plot(yillar, mac_basina_atilan_gol_values, "b-*")
        plt.xlabel("Yıllar")
        plt.ylabel("Maç Başına Atılan Gol")
        plt.title("Yıllara Göre Maç Başına Atılan Gol Grafiği")
        st.pyplot(plt)

    st.header("Grafikler Hakkında Yorumlar")
    st.write("1-Takımımızın grafiklere bakarak 2014-2018 yılları arasında belirgin bir şekilde topla oynama yüzdesinin azaldığını görmekteyiz.")
    st.write("2-Takımızın pas isabet yüzdesinin 2016 yılına kadar düşüş gözlenirken 2016 yılından sonra "
                 "2020 yılına kadar kademeli bir artış "
                 "görmekteyiz aynı zamanda pas isabet yüzdesinin zirve yaptığı dönemde takımımızın diğer değerlere de pozitif bir etki"
                 "yaptığını görmekteyiz.")
    st.write("3-Takımızın ortalama şut ve başarılı orta ortalamasının arasında doğrudan bir ilişki gözlemleniyor."
                 "Bu iki değerde oldukça değişken değerler.")
    st.write("4-Birçok grafikte 2019-2020 istatistiklerinde değişikler gözüküyor muhtemelen bu sezonlarda "
                 "takım, teknik direktör, oyun anlayışı tarzı istatistikleri etkileyecek değişiklikler olmuş olabilir.")
    st.write("5-Grafiklerde genel olarak uzun vadeli performans trendleri incelendiğinde,"
                 " bazı alanlarda (örneğin, pas isabeti) iyileşme görülse de, "
                 "genel olarak takımın istikrarlı bir performans sergilemekte zorlandığı gözlemleniyor.")
