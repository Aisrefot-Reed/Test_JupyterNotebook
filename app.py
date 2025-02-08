import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="Data Analysis App", layout="wide")

# Функция для генерации тестовых данных
def generate_test_data(rows=100):
    dates = pd.date_range(start='2024-01-01', periods=rows, freq='D')
    categories = ['A', 'B', 'C', 'D']
    
    data = {
        'Date': dates,
        'Category': [random.choice(categories) for _ in range(rows)],
        'Value': np.random.normal(100, 15, rows),
        'Quantity': np.random.randint(1, 100, rows),
        'Customer_ID': np.random.randint(1000, 9999, rows)
    }
    
    return pd.DataFrame(data)

# Функция для анализа данных
def analyze_data(df):
    results = {
        'total_sales': df['Value'].sum(),
        'avg_value': df['Value'].mean(),
        'total_quantity': df['Quantity'].sum(),
        'unique_customers': df['Customer_ID'].nunique(),
        'category_distribution': df['Category'].value_counts()
    }
    return results

# Основной интерфейс
def main():
    st.title("📊 Интерактивный анализ данных")
    
    # Боковая панель
    st.sidebar.header("Настройки")
    rows = st.sidebar.slider("Количество строк данных", 50, 500, 100)
    
    # Генерация данных
    if st.sidebar.button("Сгенерировать новые данные"):
        st.session_state.df = generate_test_data(rows)
    
    if 'df' not in st.session_state:
        st.session_state.df = generate_test_data(rows)
    
    df = st.session_state.df
    
    # Отображение данных
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Просмотр данных")
        st.dataframe(df)
    
    with col2:
        st.subheader("📈 Основные метрики")
        metrics = analyze_data(df)
        
        st.metric("Общие продажи", f"${metrics['total_sales']:,.2f}")
        st.metric("Средняя стоимость", f"${metrics['avg_value']:,.2f}")
        st.metric("Всего единиц", f"{metrics['total_quantity']:,}")
        st.metric("Уникальных клиентов", metrics['unique_customers'])
    
    # Визуализации
    st.subheader("📊 Визуализация данных")
    
    # Выбор типа графика
    chart_type = st.selectbox(
        "Выберите тип графика",
        ["Линейный график", "Гистограмма", "Круговая диаграмма", "Диаграмма рассеяния"]
    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        if chart_type == "Линейный график":
            daily_sales = df.groupby('Date')['Value'].sum().reset_index()
            fig = px.line(daily_sales, x='Date', y='Value', title='Динамика продаж')
            st.plotly_chart(fig)
            
        elif chart_type == "Гистограмма":
            fig = px.histogram(df, x='Value', nbins=30, title='Распределение стоимости')
            st.plotly_chart(fig)
            
    with col4:
        if chart_type == "Круговая диаграмма":
            category_sales = df.groupby('Category')['Value'].sum()
            fig = px.pie(values=category_sales.values, names=category_sales.index, title='Продажи по категориям')
            st.plotly_chart(fig)
            
        elif chart_type == "Диаграмма рассеяния":
            fig = px.scatter(df, x='Value', y='Quantity', color='Category', title='Стоимость vs Количество')
            st.plotly_chart(fig)
    
    # Экспорт данных
    st.subheader("💾 Экспорт данных")
    if st.button("Скачать данные как CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Подтвердить скачивание",
            data=csv,
            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()