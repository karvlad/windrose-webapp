# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from windrose import WindroseAxes
from io import BytesIO

st.set_page_config(page_title="Windrose maker", layout="centered")
st.title("Генератор розы ветров")
user_title = st.text_input('Заголовок розы (ветер\течения\волн таких-то станций)')
user_legend = st.text_input('Подпись легенды (скорость\высота ветра\течения)')
uploaded_file = st.file_uploader("📂 Загрузите Excel-файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("### Предпросмотр данных:")
        st.dataframe(df.head())

        if {"deg", "speed"}.issubset(df.columns):
            fig = plt.figure(figsize=(8, 8))
            ax = WindroseAxes.from_ax(fig=fig)
            max_speed = df["speed"].max()
            if max_speed <= 2:
                bins = [0.5, 1, 1.5, 2]
            else:
                bins = [0, 2, 4, 6, 8]
            ax.bar(df["deg"].values, df["speed"].values, normed=True, bins=bins)
            ax.set_xticklabels(["В", "СВ", "С", "СЗ", "З", "ЮЗ", "Ю", "ЮВ"])
            ax.set_title(user_title)
            ax.set_legend(title=user_legend, bbox_to_anchor=(0.8, -0.15))
            fmt = "%.0f%%"
            yticks = mtick.FormatStrFormatter(fmt)
            ax.yaxis.set_major_formatter(yticks)
            ax.text(0.75, -0.18, "% - Процент повторяемости", transform=ax.transAxes)

            st.pyplot(fig)

            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="📥 Скачать график (PNG)",
                data=buf.getvalue(),
                file_name=user_title,
                mime="image/png"
            )
        else:
            st.error("В файле должны быть столбцы `deg` (направление) и `speed` (скорость).")
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")
else:
    st.info("Загрузите файл Excel для построения розы ветров.")
