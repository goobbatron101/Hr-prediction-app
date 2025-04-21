import streamlit as st
from model import predict_home_runs

st.title("HR Prediction Debug Mode")

if st.button("Refresh Predictions"):
    st.write(">>> Getting predictions...")

    try:
        df = predict_home_runs()
        st.write(">>> Done.")

        # Step 3: Filters
        min_iso = st.slider("Minimum ISO", 0.1, 0.6, 0.2)
        min_hr = st.slider("Minimum HR", 0, 30, 5)
        df = df[(df["iso"] >= min_iso) & (df["hr"] >= min_hr)]

        # Recommendation Tier Logic
        def recommend_tier(row):
            if row['iso'] >= 0.3 and row['hr'] >= 10:
                return "Bet"
            elif row['iso'] >= 0.2 and row['hr'] >= 5:
                return "Watch"
            else:
                return "Fade"

        df["Recommendation"] = df.apply(recommend_tier, axis=1)

        # Sort and rename
        df_sorted = df.sort_values(by='hr', ascending=False).reset_index(drop=True)
        df_sorted = df_sorted.rename(columns={
            "player": "Player",
            "team": "Team",
            "pitcher": "Opposing Pitcher",
            "slg": "SLG",
            "iso": "ISO",
            "hr": "HR",
            "Recommendation": "Tier"
        })

        # Style
        styled = df_sorted.style\
            .bar(subset=["SLG", "ISO"], color="#FFA07A")\
            .highlight_max(subset=["HR"], color="#90ee90")\
            .set_properties(**{"text-align": "left"})

        st.write("### Recommended HR Targets")
        st.dataframe(styled, use_container_width=True)

    except Exception as e:
        import traceback
        st.error("Something went wrong.")
        st.text(traceback.format_exc())