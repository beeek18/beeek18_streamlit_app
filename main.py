import streamlit as st

st.set_page_config(
    page_title="Дашборд",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Дашборд")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_apple.py", label="🍎 Котировки Apple", icon="📈")
    st.markdown(
        "Интерактивные графики цен акций Apple с фильтрацией по дате и периоду."
    )

with col2:
    st.page_link("pages/2_tips.py", label="🍽️ Анализ чаевых", icon="💰")
    st.markdown(
        "Визуализация датасета tips — зависимость чаевых от различных факторов."
    )
