import streamlit as st
from model import predict_home_runs
import pandas as pd

st.title("Gooby's HR Prediction App")

if st.button("Refresh Predictions"):
    st.write(">>> Getting predictions...")

    try:
        df = predict_home_runs()
        st.write(">>> Done.")

        # Filters based on xSLG and xHR
        min_xslg = st.slider("Minimum xSLG", 0.2, 0.9, 0.4)
        min_xhr = st.slider("Minimum xHR", 0, 10, 1)

        df = df[(df["xslg"] >= min_xslg) & (df["xhr"] >= min_xhr)]

        # Tier Recommendation
        def recommend_tier(row):
            if row['xhr'] >= 5 and row['xslg'] >= 0.5:
                return "Bet"
            elif row['xhr'] >= 3:
                return "Watch"
            else:
                return "Fade"

        df["Tier"] = df.apply(recommend_tier, axis=1)

        # Sort and rename for display
        df_sorted = df.sort_values(by='hr_prob', ascending=False).reset_index(drop=True)
        df_sorted = df_sorted.rename(columns={
            "player": "Player",
            "team": "Team",
            "pitcher": "Opposing Pitcher",
            "xhr": "xHR",
            "xslg": "xSLG",
            "ev": "EV",
            "la": "LA",
            "hr": "HR",
            "hr_prob": "HR Probability"
        })

        # Highlight function for tiers
        def highlight_tier(val):
            color = {
                "Bet": "#c6f5c6",
                "Watch": "#fffac8",
                "Fade": "#f5c6c6"
            }.get(val, "white")
            return f"background-color: {color}"

        # Styling
        styled = df_sorted.style\
            .bar(subset=["xHR", "xSLG", "EV", "HR Probability"], color="#ffa07a")\
            .highlight_max(subset=["HR Probability"], color="#90ee90")\
            .applymap(highlight_tier, subset=["Tier"])\
            .set_properties(**{"text-align": "left"})

        st.write("### Recommended HR Targets")
        st.dataframe(styled, use_container_width=True)

    except Exception as e:
        import traceback
        st.error("Something went wrong.")
        st.text(traceback.format_exc())

else:
    st.info("Click 'Refresh Predictions' to see today's top HR targets.")