import streamlit as st
import json
import os
import urllib.parse
from datetime import date

# Налаштування сторінки
st.set_page_config(page_title="Auto Pro Manager", page_icon="🚘", layout="wide")

# ФУНКЦІЇ ЗБЕРЕЖЕННЯ
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

garage = load_data("garage.json")
history = load_data("history.json")

st.title("🚘 Auto Pro Manager")
tab1, tab2, tab3 = st.tabs(["🗂 Мій Гараж", "🛒 Розумний пошук", "📖 Сервіс"])

# 1. ГАРАЖ
# --- ВКЛАДКА 1: ГАРАЖ ---
with tab1:
    st.subheader("➕ Додати авто в парк")
    with st.form("add_car_form"):
        c1, c2 = st.columns(2)
        with c1:
            # Тепер можна вписати ЛЮБУ марку вручну!
            brand = st.text_input("Марка", placeholder="напр. Citroen, Tesla, MAN")
            model = st.text_input("Модель", placeholder="напр. Jumper, Q7")
        with c2:
            year = st.number_input("Рік випуску", min_value=1900, max_value=2026, value=2014)
            vin = st.text_input("VIN-код", placeholder="17 символів")
            
        if st.form_submit_button("💾 Зберегти в Гараж"):
            if brand and model:
                garage.append({"Марка": brand, "Модель": model, "VIN": vin, "Рік": year})
                save_data(garage, "garage.json")
                st.success(f"✅ {brand} {model} успішно додано!")
                st.rerun()
            else:
                st.error("🚨 Впиши хоча б марку та модель!")

    for i, car in enumerate(garage):
        st.write(f"---")
        st.write(f"🚙 **{car['Марка']} {car['Модель']} ({car['Рік']})** | VIN: `{car['VIN']}`")

# 2. ПОШУК (з посиланням на всі сайти)
with tab2:
    st.subheader("🔍 Пошук запчастин по всьому ринку")
    if garage:
        sel_car = st.selectbox("Обери авто:", garage, format_func=lambda x: f"{x['Марка']} {x['Модель']}")
        part = st.text_input("Назва деталі:", placeholder="Наприклад: датчик дверей")
        
        if part:
            p_enc = urllib.parse.quote_plus(part)
            v_enc = urllib.parse.quote_plus(sel_car['VIN'])
            
            st.write("🌍 Оберіть магазин для перевірки:")
            cols = st.columns(4)
            cols[0].markdown(f"[🔵 Oscaro (FR)](https://www.oscaro.com/fr/search?q={p_enc})")
            cols[1].markdown(f"[🛠 Avto.pro](https://avto.pro/search/?q={v_enc}+{p_enc})")
            cols[2].markdown(f"[📦 Exist.ua](https://exist.ua/uk/search/?text={p_enc})")
            cols[3].markdown(f"[🏎 Baza.com](https://baza.com/search?q={p_enc})")
    else:
        st.info("Спочатку додайте авто в Гараж.")

# 3. СЕРВІСНА КНИЖКА
with tab3:
    st.subheader("🛠 Історія обслуговування")
    if garage:
        sel_h = st.selectbox("Авто:", garage, format_func=lambda x: f"{x['Марка']} {x['Модель']}", key="h_box")
        with st.form("h_form"):
            work = st.text_input("Що робили?")
            cost = st.number_input("Ціна (грн):")
            if st.form_submit_button("Додати запис"):
                history.append({"car": sel_h['Модель'], "work": work, "cost": cost})
                save_data(history, "history.json")
                st.rerun()
        
        for h in history:
            if h['car'] == sel_h['Модель']:
                st.write(f"✅ {h['work']} — **{h['cost']} грн**")
