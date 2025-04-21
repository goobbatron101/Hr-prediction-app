import streamlit as st
from model import predict_home_runs

st.title("HR Prediction Debug Mode")

if st.button("Refresh Predictions"):
    st.write(">>> Getting predictions...")
    try:
        df = predict_home_runs()
        st.write(">>> Done.")
        # Sort by slugging or HR
df_sorted = df.sort_values(by='hr', ascending=False).reset_index(drop=True)

# Style the table
styled = df_sorted.style\
    .bar(subset=["slg", "iso"], color="#FFA07A")\
    .highlight_max(subset=["hr"], color="#90ee90")\
    .set_properties(**{"text-align": "left"})

st.write("### Recommended HR Targets")
st.dataframe(styled, use_container_width=True)
    except Exception as e:
        import traceback
        st.error("Something went wrong.")
        st.text(traceback.format_exc())
else:
    st.info("Click the button to load predictions.")