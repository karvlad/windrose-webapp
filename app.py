# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from windrose import WindroseAxes
from io import BytesIO
from matplotlib import font_manager

plt.rcParams["font.family"] = 'dejavu serif'

st.set_page_config(page_title="Windrose maker", layout="centered")
st.title("Генератор розы ветров")
user_title = st.text_input('Заголовок розы (ветер\течения\волн таких-то станций)')
user_legend = st.text_input('Подпись легенды (скорость\высота ветра\течения)')
uploaded_file = st.file_uploader("📂 Загрузите Excel-файл", type=["xlsx", "xls"])

directions = ["В", "ВСВ", "СВ", "ССВ", "С", "ССЗ", "СЗ", "ЗСЗ","З", "ЗЮЗ", "ЮЗ", "ЮЮЗ", "Ю", "ЮЮВ", "ЮВ", "ВЮВ"]
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("### Предпросмотр данных:")
        st.dataframe(df.head())


        if {"deg", "value"}.issubset(df.columns):
            fig = plt.figure(figsize=(8, 8))
            ax = WindroseAxes.from_ax(fig=fig)
            max_value = df["value"].max()
            if max_value <= 2:
                bins = [0, 0.5, 1, 1.5, 2]
            else:
                bins = [0, 2, 4, 6, 8]
            ax.bar(df["deg"].values, df["value"].values, normed=True, bins=bins)
            #ax.set_xticklabels(["В", "ВСВ", "СВ", "ССВ", "С", "ССЗ", "СЗ", "ЗСЗ", "З", "ЗЮЗ", "ЮЗ", "ЮЮЗ", "Ю", "ЮЮВ", "ЮВ", "ВЮВ"])
            #ax.set_thetagrids([0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5,180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5],labels=directions)
            ax.set_thetagrids([0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5,180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5],labels=directions)
            ax.set_title(user_title)
            ax.set_legend(title=user_legend, bbox_to_anchor=(0.8, -0.15))
            fmt = "%.0f%%"
            yticks = mtick.FormatStrFormatter(fmt)
            ax.yaxis.set_major_formatter(yticks)
            for label in ax.get_yticklabels():
                label.set_fontsize(8)
            ax.text(0.75, -0.18, "% - Процент повторяемости", transform=ax.transAxes)


            st.pyplot(fig)

            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="📥 Скачать график (PNG)",
                data=buf.getvalue(),
                file_name=f'{user_title}.png',
                mime="image/png"
            )
        else:
            st.error("В файле должны быть столбцы `deg` (направление в градусах) и `value` (скорость ветра\течения или высота волны).")
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")
else:
    st.info("Загрузите файл Excel для построения розы ветров.")
