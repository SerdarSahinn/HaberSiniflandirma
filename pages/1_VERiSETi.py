import streamlit as st
import pandas as pd
df = pd.read_csv("7allV03.csv")


columns={"category":"KATEGORİ","text":"HABER METNİ"}
df=df.rename(columns=columns)
st.dataframe(df)
