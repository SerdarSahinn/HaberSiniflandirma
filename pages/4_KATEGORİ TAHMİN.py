import streamlit as st
import pandas as pd
import joblib
import numpy as np


# HTML BUTON KODLARIMIZ

colors = ['#C6A969', '#597E52', '#756AB6', '#BF3131', '#3887BE', '#E36414', '#88AB8E']

html_code = """
<div style="display: flex; justify-content: space-between;">
    <button style="width: 100px; background-color: {color1};">SİYASET</button>
    <button style="width: 100px; background-color: {color2};">DÜNYA</button>
    <button style="width: 100px; background-color: {color3};">EKONOMİ</button>
    <button style="width: 100px; background-color: {color4};">KÜLTÜR</button>
    <button style="width: 100px; background-color: {color5};">SAĞLIK</button>
    <button style="width: 100px; background-color: {color6};">SPOR</button>
    <button style="width: 100px; background-color: {color7};">TEKNOLOJİ</button>
</div>
"""

st.markdown(html_code.format(color1=colors[0], color2=colors[1], color3=colors[2],
                              color4=colors[3], color5=colors[4], color6=colors[5], color7=colors[6]), unsafe_allow_html=True)



# KAYDETTİĞİMİZ MODELLERİ YÜKLÜYORUZ
model=joblib.load("modellim.pkl")
loaded_count_vect = joblib.load('count_vectorizer.pkl')
loaded_tfidf_transformer = joblib.load('tfidf_transformer.pkl')



#KULLANICININ GİRDİĞİ METNİ ALIP ,TF-IDF VE COUNTVECTORIZER İLE VEKTÖRLEŞTİRİYORUZ
user_input=st.text_area("HABER METNİNİ GİRİNİZ",placeholder="HABER METNİNİ GİRİNİZ",height=250)
input_vectorized = loaded_count_vect.transform([user_input])
input_tfidf = loaded_tfidf_transformer.transform(input_vectorized)


# TAHMİN ET BUTONUNA TIKLANDIĞINDA PREDICT YAPILMASI VE SONUCUNUN EKRANA YAZILMASI
if st.button("KATEGORİ TAHMİNİ İÇİN TIKLAYIN",key="my_button"): 
    tahmin = model.predict(input_tfidf)
    predicted_category=tahmin[0].upper()
    st.write(f"<p style='color:#F7DC6F; font-size:20px; font-family: monospace, sans-serif;'> KATEGORİ : {predicted_category}</p>", unsafe_allow_html=True)
