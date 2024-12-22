import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Функция для главной страницы
def main_page():
    st.title("Платформа управления водными ресурсами")
    st.image("Lednik-fedchenko.jpg", caption="Эффективное управление водой", )
    st.markdown("""
    Эта платформа помогает анализировать, прогнозировать и оптимизировать использование водных ресурсов. 
    Вдохновленная инициативами устойчивого развития, наша цель — предложить фермерам и управленцам современные технологии для решения проблем вододефицита.
    """)

# Функция для страницы "О нас"
def about_page():
    st.title("О нас")
    st.markdown("""
    Мы — команда энтузиастов, работающая над решением одной из самых важных глобальных проблем — водного кризиса.
    С использованием современных технологий, таких как искусственный интеллект и машинное обучение, мы предлагаем инновационные решения 
    для управления водными ресурсами.
    """)    

# Функция для страницы анализа данных
def data_analysis_page():
    st.title("Анализ данных")
    uploaded_file = st.file_uploader("Загрузите файл с данными о водопотреблении (CSV)", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Загруженные данные:")
        st.dataframe(data)

        # График данных
        st.header("График зависимости водопотребления от времени")
        if 'time' in data.columns and 'consumption' in data.columns:
            data['time'] = pd.to_datetime(data['time'])
            plt.figure(figsize=(10, 5))
            plt.plot(data['time'], data['consumption'], label="Водопотребление", color="blue")
            plt.xlabel("Время")
            plt.ylabel("Водопотребление")
            plt.legend()
            st.pyplot(plt)
        else:
            st.warning("Пожалуйста, убедитесь, что в данных есть колонки 'time' и 'consumption'.")

        # Прогнозирование
        st.header("Прогнозирование водопотребления")
        if 'time' in data.columns and 'consumption' in data.columns:
            try:
                data['time_ordinal'] = data['time'].map(lambda x: x.toordinal())
                X = np.array(data['time_ordinal']).reshape(-1, 1)
                y = np.array(data['consumption'])

                model = LinearRegression()
                model.fit(X, y)

                future_time = pd.date_range(start=data['time'].max(), periods=30, freq='D')
                future_time_ordinal = future_time.map(lambda x: x.toordinal()).values.reshape(-1, 1)
                predictions = model.predict(future_time_ordinal)

                plt.figure(figsize=(10, 5))
                plt.plot(data['time'], data['consumption'], label="Исторические данные", color="blue")
                plt.plot(future_time, predictions, label="Прогноз", color="green")
                plt.xlabel("Дата")
                plt.ylabel("Водопотребление")
                plt.legend()
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Ошибка в обработке данных: {e}")
        else:
            st.warning("Добавьте колонки 'time' и 'consumption' для выполнения прогнозирования.")
    else:
        st.info("Загрузите файл, чтобы начать анализ.")

# Функция для страницы рекомендаций
def recommendations_page():
    st.title("Рекомендации для фермеров")
    st.markdown("""
    На основе анализа данных о водопотреблении мы предлагаем следующие рекомендации:
    - Используйте **капельное орошение** для экономии воды.
    - Планируйте полив с учетом прогноза погоды.
    - Устанавливайте датчики для мониторинга влажности почвы.
    - Регулярно проверяйте состояние оборудования для предотвращения утечек.
    """)

# Меню приложения
menu = st.sidebar.radio("Меню", ["Главная", "О нас", "Анализ данных", "Рекомендации"])

if menu == "Главная":
    main_page()
elif menu == "О нас":
    about_page()
elif menu == "Анализ данных":
    data_analysis_page()
elif menu == "Рекомендации":
    recommendations_page()
