import requests
import streamlit as st


# HTML BUTON VE RENK ETİKETLERİ

colors = ['#B15EFF', '#CE5A67', '#6C5F5B', '#192655', '#DE8F5F']

html_code = """
<div style="display: flex; justify-content: space-between; height:35px">
    <button style="width: 150px; background-color: {color1};">EKONOMİ</button>
    <button style="width: 150px; background-color: {color2};">KÜLTÜR SANAT</button>
    <button style="width: 150px; background-color: {color3};">POLİTİKA</button>
    <button style="width: 150px; background-color: {color4};">EĞİTİM</button>
    <button style="width: 150px; background-color: {color5};">DÜNYA</button>
    
    
</div>
"""
# HTML KODUNU GÖRÜNTÜLEME
st.markdown(html_code.format(color1=colors[0], color2=colors[1], color3=colors[2],
                              color4=colors[3], color5=colors[4]), unsafe_allow_html=True)



colors = ['#C6A969', '#597E52', '#756AB6', '#BF3131', '#3887BE']

html_code = """
<div style="display: flex; justify-content: space-between;height:35px">
    <button style="width: 150px; background-color: {color1};">TEKNOLOJİ</button>
    <button style="width: 150px; background-color: {color2};">MAGAZİN</button>
    <button style="width: 150px; background-color: {color3};">SAĞLIK</button>
    <button style="width: 150px; background-color: {color4};">GÜNDEM</button>
    <button style="width: 150px; background-color: {color5};">SPOR</button>
    
</div>
"""

st.markdown(html_code.format(color1=colors[0], color2=colors[1], color3=colors[2],
                              color4=colors[3], color5=colors[4]), unsafe_allow_html=True)


kullanici_metni=st.text_area("HABER METNİNİ GİRİNİZ",placeholder="HABER METNİNİ GİRİNİZ",height=250)

# API İLE MODEL ÇEKME
API_URL = "https://api-inference.huggingface.co/models/serdarakyol/interpress-turkish-news-classification"
API_TOKEN = "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"   # Hugginface API keyimiz
headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()



# Butona tıklandığında kullanıcın inputunu modele gönderiyoruz
# model bize iç içe dict ler döndürüyor. Biz en olası 2 kategoriyi seçtiğimizde dolayı data[0][0] ve data[0][1] şeklinde alıyoruz
if st.button("KATEGORİ TAHMİNİ İÇİN TIKLAYIN"):
    data = query({
    "inputs":kullanici_metni,
})
    tahmin1=data[0][0]["label"]  # en yüksek yüzdeli tahmin kategorisi
    tahmin11=tahmin1.upper()
    olasilik1=data[0][0]["score"]   # tahminin skoru
    olasilik1=round(olasilik1,2)
 
    tahmin2=data[0][1]["label"]    #en yüksek yüzdeli 2. tahmin kategorisi
    tahmin22=tahmin2.upper()
    olasilik2=data[0][1]["score"]   # tahmin skoru
    olasilik2=round(olasilik2,2)

    # ekrana sonuçların verilmesi
    st.write(f"YÜZDE  <span style='color:#4942E4; font-size:20px; font-family: monospace, sans-serif;'>   {olasilik1}    OLASILIKLA  </span>   <span style='color:#F7DC6F; font-size:20px; font-family: monospace, sans-serif;'> {tahmin11}</span>  kategorisine aittir", unsafe_allow_html=True)
    st.write(f"YÜZDE  <span style='color:#4942E4; font-size:20px; font-family: monospace, sans-serif;'>   {olasilik2}    OLASILIKLA  </span>   <span style='color:#F7DC6F; font-size:20px; font-family: monospace, sans-serif;'> {tahmin22}</span>  kategorisine aittir", unsafe_allow_html=True)
