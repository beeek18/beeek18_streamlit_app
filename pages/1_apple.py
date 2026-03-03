import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io

st.set_page_config(page_title="Котировки Apple", page_icon="🍎", layout="wide")
st.title("🍎 Котировки Apple (AAPL)")
st.markdown("---")


st.sidebar.header("⚙️ Настройки")
start_date = st.sidebar.date_input("Начальная дата", value=pd.to_datetime("2023-03-01"))
end_date = st.sidebar.date_input("Конечная дата", value=pd.to_datetime("2026-03-03"))
chart_type = st.sidebar.selectbox("Тип графика", ["Линейный", "Свечной", "Область"])
show_volume = st.sidebar.checkbox("Показать объём торгов", value=True)


@st.cache_data
def load_data(start, end):
    df = yf.download("AAPL", start=start, end=end, auto_adjust=True)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df


with st.spinner("Загружаем данные..."):
    df = load_data(start_date, end_date)

if df.empty:
    st.error("Нет данных за выбранный период.")
    st.stop()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Текущая цена", f"${df['Close'].iloc[-1]:.2f}")
col2.metric("Максимум", f"${df['High'].max():.2f}")
col3.metric("Минимум", f"${df['Low'].min():.2f}")
col4.metric(
    "Изменение", f"{((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100:.1f}%"
)

st.markdown("---")

if chart_type == "Линейный":
    fig = px.line(
        df,
        x=df.index,
        y="Close",
        title="Цена закрытия AAPL",
        labels={"Close": "Цена ($)", "Date": "Дата"},
    )
elif chart_type == "Свечной":
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )
    fig.update_layout(
        title="Свечной график AAPL", xaxis_title="Дата", yaxis_title="Цена ($)"
    )
else:
    fig = px.area(
        df,
        x=df.index,
        y="Close",
        title="Цена закрытия AAPL (область)",
        labels={"Close": "Цена ($)", "Date": "Дата"},
    )

fig.update_layout(height=450)
st.plotly_chart(fig, use_container_width=True)

if show_volume:
    fig_vol = px.bar(
        df,
        x=df.index,
        y="Volume",
        title="Объём торгов",
        labels={"Volume": "Объём", "Date": "Дата"},
        color_discrete_sequence=["#636EFA"],
    )
    fig_vol.update_layout(height=250)
    st.plotly_chart(fig_vol, use_container_width=True)

st.markdown("---")
with st.expander("📄 Показать данные"):
    st.dataframe(df.tail(30), use_container_width=True)


def fig_to_png(df, column="Close", title="AAPL"):
    fig_mpl, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df[column], color="#636EFA", linewidth=1.5)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Дата")
    ax.set_ylabel("Цена ($)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    fig_mpl.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig_mpl)
    return buf


buf = fig_to_png(df, title="Котировки AAPL")
st.download_button(
    "📥 Скачать график (PNG)", data=buf, file_name="apple_chart.png", mime="image/png"
)
