import streamlit as st
from model import predict_home_runs

st.title("HR Prediction Debug Mode")

if st.button("Refresh Predictions"):
    st.write(">>> Getting predictions...")
    try:
        df = predict_home_runs()
        st.write(">>> Done.")
        st.dataframe(df)
    except Exception as e:
        import traceback
        st.error("Something went wrong.")
        st.text(traceback.format_exc())
else:
    st.info("Click the button to load predictions.")