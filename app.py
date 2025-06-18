# app.py

import streamlit as st
import pandas as pd
from windrose import WindroseAxes
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Windrose Plot Generator", layout="centered")
st.title("🌬️ Windrose Plot Generator")
st.markdown("Upload your CSV with `wd` (wind direction) and `ws` (wind speed) columns.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, decimal=',', delimiter=';')
        st.write("### Preview of uploaded data:")
        st.dataframe(df.head())

        if 'ws' in df.columns and 'wd' in df.columns:
            fig = plt.figure(figsize=(8, 8))
            ax = WindroseAxes.from_ax(fig=fig)
            ax.bar(df['wd'], df['ws'])
            ax.set_legend()
            st.pyplot(fig)

            buf = BytesIO()
            fig.savefig(buf, format="png")
            st.download_button(
                label="📥 Download Windrose Plot (PNG)",
                data=buf.getvalue(),
                file_name="windrose_plot.png",
                mime="image/png"
            )
        else:
            st.error("Your CSV must include columns named `wd` (wind direction) and `ws` (wind speed).")
    except Exception as e:
        st.error(f"Error reading file: {e}")
