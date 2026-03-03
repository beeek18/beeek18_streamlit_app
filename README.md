# 📊 Streamlit Dashboard — Apple & Tips

Многостраничное веб-приложение на Streamlit с двумя разделами:
- 🍎 Котировки акций Apple с интерактивными графиками
- 🍽️ Анализ датасета чаевых (tips)

## 🚀 Запуск через Docker

### 1. Клонируй репозиторий
```bash
git clone https://github.com/beeek18/beeek18_streamlit_app.git
cd beeek18_streamlit_app
```

### 2. Создай `.env` файл
```bash
cp .env.example .env
```

### 3. Запусти
```bash
docker compose up --build -d
```

### 4. Открой в браузере
```
http://localhost:8501
```

### 5. Остановка
```bash
docker compose down
```

---

## 💻 Запуск локально (без Docker)
```bash
uv sync
uv run streamlit run main.py
```

---

## 📁 Структура проекта
```
beeek18_streamlit_app/
├── pages/
│   ├── 1_apple.py       # котировки Apple
│   └── 2_tips.py        # анализ чаевых
├── data/
│   └── tips.csv
├── main.py              # главная страница
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

---

## 📈 Страницы

### 🍎 Котировки Apple
- Выбор периода через sidebar
- Три типа графиков: линейный, свечной, область
- График объёма торгов
- Метрики: текущая цена, максимум, минимум, изменение
- Скачать график в PNG

### 🍽️ Анализ чаевых
- Загрузка своего CSV файла
- Фильтрация по дню недели и времени
- Scatter, box, histogram — через Plotly
- Heatmap корреляций — через Seaborn
- Скачать график в PNG

---

## 🛠 Стек

- [Streamlit](https://streamlit.io) — веб-фреймворк
- [yfinance](https://pypi.org/project/yfinance/) — данные с Yahoo Finance
- [Plotly](https://plotly.com/python/) — интерактивные графики
- [Pandas](https://pandas.pydata.org) — обработка данных
- [Seaborn](https://seaborn.pydata.org) — статистические графики
- [Docker](https://www.docker.com) — контейнеризация