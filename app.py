import streamlit as st
import pandas as pd
from model import predict_home_runs
from data_loader import load_batter_features

st.set_page_config(page_title="MLB HR Predictor", layout="wide")
st.title("Daily Home Run Predictions")

if st.button("Refresh Predictions"):
    data = load_batter_features()
    predictions = predict_home_runs(data)
st.write("Showing predictions (raw):")
st.dataframe(predictions)
else:
    st.info("Click the button above to load today's predictions.")
