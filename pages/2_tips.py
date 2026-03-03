import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import io

st.set_page_config(page_title="Анализ чаевых", page_icon="🍽️", layout="wide")
st.title("🍽️ Анализ чаевых")
st.markdown("---")

st.sidebar.header("⚙️ Настройки")
uploaded_file = st.sidebar.file_uploader("Загрузить CSV", type=["csv"])


@st.cache_data
def load_data(file=None):
    if file:
        return pd.read_csv(file, encoding="latin-1")
    return pd.read_csv("data/tips.csv")


df = load_data(uploaded_file)

required_cols = {"total_bill", "tip", "sex", "size", "day", "time"}
if not required_cols.issubset(df.columns):
    st.error(f"В файле не хватает колонок: {required_cols - set(df.columns)}")
    st.stop()

days = st.sidebar.multiselect(
    "День недели",
    options=df["day"].unique().tolist(),
    default=df["day"].unique().tolist(),
)
times = st.sidebar.multiselect(
    "Время", options=df["time"].unique().tolist(), default=df["time"].unique().tolist()
)

df_filtered = df[df["day"].isin(days) & df["time"].isin(times)]

col1, col2, col3 = st.columns(3)
col1.metric("Всего записей", len(df_filtered))
col2.metric("Средний чаевой", f"${df_filtered['tip'].mean():.2f}")
col3.metric("Средний счёт", f"${df_filtered['total_bill'].mean():.2f}")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.scatter(
        df_filtered,
        x="total_bill",
        y="tip",
        color="sex",
        size="size",
        title="Счёт vs Чаевые",
        labels={"total_bill": "Счёт ($)", "tip": "Чаевые ($)"},
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(
        df_filtered,
        x="day",
        y="tip",
        color="time",
        title="Чаевые по дням недели",
        labels={"day": "День", "tip": "Чаевые ($)"},
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig3 = px.histogram(
        df_filtered,
        x="tip",
        nbins=20,
        color="sex",
        title="Распределение чаевых",
        labels={"tip": "Чаевые ($)"},
        barmode="overlay",
        opacity=0.7,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4, ax = plt.subplots(figsize=(6, 4))
    corr = df_filtered[["total_bill", "tip", "size"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Корреляция числовых признаков")
    st.pyplot(fig4)

st.markdown("---")
with st.expander("📄 Показать данные"):
    st.dataframe(df_filtered, use_container_width=True)


def fig_to_png(fig_plotly, title="chart"):
    fig_mpl, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(
        df_filtered["total_bill"], df_filtered["tip"], alpha=0.6, color="#636EFA"
    )
    ax.set_xlabel("Счёт ($)")
    ax.set_ylabel("Чаевые ($)")
    ax.set_title(title)
    plt.tight_layout()
    buf = io.BytesIO()
    fig_mpl.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig_mpl)
    return buf


buf = fig_to_png(fig1, title="Счёт vs Чаевые")
st.download_button(
    "📥 Скачать график (PNG)",
    data=buf,
    file_name="tips_chart.png",
    mime="image/png",
)
