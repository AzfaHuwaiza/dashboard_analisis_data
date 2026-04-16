import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("E-Commerce Public Dataset Dashboard")
st.markdown("Dashboard ini menampilkan analisis revenue dan distribusi pelanggan.")

@st.cache_data
def load_data():
    data = pd.read_csv("dashboard_data.csv")
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    return data

data = load_data()

st.sidebar.header("Filter")

selected_state = st.sidebar.selectbox(
    "Pilih State",
    options=data['customer_state'].unique()
)

filtered_data = data[data['customer_state'] == selected_state]

st.subheader("Top 10 Kategori dengan Revenue Tertinggi")

revenue_category = filtered_data.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots()
revenue_category.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Distribusi Pelanggan per State")

customer_state = data['customer_state'].value_counts().head(10)

fig2, ax2 = plt.subplots()
customer_state.plot(kind='bar', ax=ax2)
st.pyplot(fig2)
