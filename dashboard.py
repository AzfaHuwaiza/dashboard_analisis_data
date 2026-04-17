import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

def load_data():
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['year'] = df['order_purchase_timestamp'].dt.year
    return df

all_data = load_data()

with st.sidebar:
    st.header("Filter Data")
    selected_year = st.selectbox("Pilih Tahun Analisis", [2017, 2018])

main_df = all_data[all_data['year'] == selected_year]
prev_df = all_data[all_data['year'] == (selected_year - 1)]

st.header('E-Commerce Public Dashboard 🛒')

st.subheader(f'Top 5 Kategori Produk Berdasarkan Revenue ({selected_year})')
revenue_df = main_df.groupby('product_category_name')['price'].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x='price', y='product_category_name', data=revenue_df.sort_values(by='price', ascending=False).head(5), palette=colors, ax=ax1)
ax1.set_xlabel('Total Revenue')
ax1.set_ylabel('Kategori Produk')
st.pyplot(fig1)

st.subheader(f'Demografi & Pertumbuhan Pelanggan ({selected_year} vs {selected_year - 1})')
curr_cust = main_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
curr_cust.rename(columns={'customer_unique_id': 'curr_year'}, inplace=True)

prev_cust = prev_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
prev_cust.rename(columns={'customer_unique_id': 'prev_year'}, inplace=True)

growth_df = pd.merge(curr_cust, prev_cust, on='customer_state', how='left').fillna(0)
growth_df['growth'] = growth_df['curr_year'] - growth_df['prev_year']

fig2, ax2 = plt.subplots(1, 2, figsize=(20, 6))
sns.barplot(x='curr_year', y='customer_state', data=growth_df.sort_values('curr_year', ascending=False).head(5), palette=colors, ax=ax2[0])
ax2[0].set(title=f'Top 5 State ({selected_year})', xlabel='Jumlah Pelanggan', ylabel='State')

sns.barplot(x='growth', y='customer_state', data=growth_df.sort_values('growth', ascending=False).head(5), palette=colors, ax=ax2[1])
ax2[1].set(title=f'Pertumbuhan Tertinggi ({selected_year - 1} ke {selected_year})', xlabel='Pertumbuhan', ylabel='State')
st.pyplot(fig2)
