import streamlit as st
from data_loader import load_batter_features
from model import predict_home_runs

st.title("HR Prediction Debug Test")

if st.button("Refresh Predictions"):
    st.write(">>> Running prediction logic...")
    try:
        data = load_batter_features()
        predictions = predict_home_runs(data)
        st.dataframe(predictions)  # NO styling, just raw output
    except Exception as e:
        import traceback
        st.error("Something went wrong!")
        st.text(traceback.format_exc())
else:
    st.info("Click the button to generate predictions.")
