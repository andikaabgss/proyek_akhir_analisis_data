import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
import folium
sns.set_style("whitegrid")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/main_df.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
    return df

main_df = load_data()

# Sidebar filters
st.sidebar.header("Filter")

# Date range filter
min_date = main_df['order_purchase_timestamp'].min().date()
max_date = main_df['order_purchase_timestamp'].max().date()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = main_df[(main_df['order_purchase_timestamp'].dt.date >= start_date) & 
                         (main_df['order_purchase_timestamp'].dt.date <= end_date)]
elif isinstance(date_range, tuple) and len(date_range) == 1:
    # Single date selected
    selected_date = date_range[0]
    filtered_df = main_df[main_df['order_purchase_timestamp'].dt.date == selected_date]
else:
    filtered_df = main_df

# State filter
states = sorted(filtered_df['customer_state'].unique())
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian",
    options=states,
    default=states[:5] if len(states) > 5 else states  # Default to first 5 states
)

if selected_states:
    filtered_df = filtered_df[filtered_df['customer_state'].isin(selected_states)]

# Product category filter
categories = sorted(filtered_df['product_category_name'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=categories,
    default=[]
)

if selected_categories:
    filtered_df = filtered_df[filtered_df['product_category_name'].isin(selected_categories)]

# Payment type filter
payment_types = sorted(filtered_df['payment_type'].dropna().unique())
selected_payment_types = st.sidebar.multiselect(
    "Pilih Jenis Pembayaran",
    options=payment_types,
    default=payment_types
)

if selected_payment_types:
    filtered_df = filtered_df[filtered_df['payment_type'].isin(selected_payment_types)]
def create_customer_by_state(data):
    customer_by_state = data['customer_state'].value_counts().reset_index()
    
    return customer_by_state

def create_customer_by_city(data):
    customer_by_city = data['customer_city'].value_counts().reset_index()
    
    return customer_by_city

def create_sum_revenue(data):
    total_revenue = data['revenue'].sum()
    
    return total_revenue
                            
def create_avg_revenue_per_order(data):
    avg_revenue_per_order = data.groupby('order_id')['revenue'].sum().mean()
    
    return avg_revenue_per_order

def create_top_10_products_by_revenue(data):
    top_10_products = data.groupby('product_category_name')['revenue'].sum().nlargest(10).reset_index()

    
    return top_10_products

def create_top_10_products_by_quantity(data):
    top_10_products_quantity = data.groupby('product_category_name')['order_item_id'].sum().nlargest(10).reset_index()
    
    return top_10_products_quantity

def create_monthly_revenue_trend(data):
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    data['month'] = data['order_purchase_timestamp'].dt.to_period('M')
    data['month'] = data['month'].dt.strftime('%Y-%m')
    monthly_revenue_trend = data.groupby('month')['revenue'].sum().reset_index()
    
    return monthly_revenue_trend

def create_payment_type_distribution(data):
    payment_type_distribution = data['payment_type'].value_counts().reset_index()
    
    return payment_type_distribution  

def create_highest_reviewed_products(data):
    highest_reviewed_products = data.groupby('product_category_name')['review_score'].mean().nlargest(10).reset_index()
    
    return highest_reviewed_products   

def create_lowest_reviewed_products(data):
    lowest_reviewed_products = data.groupby('product_category_name')['review_score'].mean().nsmallest(10).reset_index()
    
    return lowest_reviewed_products

def create_average_review_score_by_delivery_status(data):
    data['delivery_status'] = (data['order_delivered_customer_date'] <= data['order_estimated_delivery_date']).apply(lambda x: 'Tepat Waktu' if x else 'Terlambat')
    average_review_score_by_delivery_status = data.groupby('delivery_status')['review_score'].mean().reset_index()
    
    return average_review_score_by_delivery_status

main_df = pd.read_csv("Dashboard/main_df.csv")

customer_by_state = create_customer_by_state(filtered_df)
customer_by_city = create_customer_by_city(filtered_df)
total_revenue = create_sum_revenue(filtered_df)
avg_revenue_per_order = create_avg_revenue_per_order(filtered_df)
top_10_products = create_top_10_products_by_revenue(filtered_df)
top_10_products_quantity = create_top_10_products_by_quantity(filtered_df)
monthly_revenue_trend = create_monthly_revenue_trend(filtered_df)
payment_type_distribution = create_payment_type_distribution(filtered_df)
highest_reviewed_products = create_highest_reviewed_products(filtered_df)
lowest_reviewed_products = create_lowest_reviewed_products(filtered_df)
average_review_score_by_delivery_status = create_average_review_score_by_delivery_status(filtered_df)

# Show filtered data info
st.sidebar.markdown(f"**Rekaman Terfilter:** {len(filtered_df):,}")
if isinstance(date_range, tuple) and len(date_range) == 2:
    st.sidebar.markdown(f"**Rentang Tanggal:** {date_range[0]} to {date_range[1]}")
elif isinstance(date_range, tuple) and len(date_range) == 1:
    st.sidebar.markdown(f"**Tanggal Terpilih:** {date_range[0]}")
else:
    st.sidebar.markdown("**Rentang Tanggal:** Semua tanggal")

# Refresh button
if st.sidebar.button("Reset Filter"):
    st.session_state.clear()
    st.rerun()

# Header
col1, col2 = st.columns([1, 6.5])
with col1:
    st.image("Dashboard/olist_logo.png")
with col2:
    st.title("Dashboard Olist E-commerce")  

# Metic Cards
col1, col2, col3 = st.columns([0.75, 1.25, 1], gap="medium")
with col1:
    st.metric(label="Total Pelanggan", value=f"{filtered_df['customer_id'].nunique():,}")
with col2:
    st.metric(label="Total Revenue", value=f"R$ {total_revenue:,.2f}")
with col3:
    st.metric(label="Rata-rata Revenue per Pesanan", value=f"R$ {avg_revenue_per_order:,.2f}")

# Color schemes
color_contrast = ["#184375", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5"]
color_gradient = sns.color_palette("Blues", n_colors=10)
red_gradient = sns.color_palette("Reds_r", n_colors=10)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5= st.tabs(["📈 Revenue & Tren", "👥 Pelanggan", "📦 Produk", "💳 Pembayaran", "💬 Ulasan"])

with tab1:
    # Monthly Revenue Trend
    st.subheader("Tren Revenue Bulanan")
    
    # Prepare data for plotting
    monthly_revenue = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['revenue'].sum() 
    monthly_sales = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['order_id'].nunique()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot monthly revenue
    ax1.plot(monthly_revenue.index.astype(str), monthly_revenue.values, color='blue', label='Monthly Revenue')
    ax1.set_xlabel('Bulan')
    ax1.set_ylabel('Revenue (BRL)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Tren Revenue dan Penjualan Bulanan (Satu Tahun Terakhir)')
    
    # Plot monthly sales
    ax2 = ax1.twinx()
    ax2.plot(monthly_sales.index.astype(str), monthly_sales.values, color='red', label='Monthly Sales')
    ax2.set_ylabel('Penjualan', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    ax1.set_xticklabels(monthly_revenue.index.strftime('%Y-%m'), rotation=45, ha='right')
    
    # Legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)


with tab2:   
    # Customers by State and City
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pelanggan berdasarkan Negara Bagian")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(data=customer_by_state.head(10), x='customer_state', y='count', palette=color_contrast, ax=ax)
        ax.set_xlabel("Negara Bagian")
        ax.set_ylabel("Jumlah Pelanggan")
        ax.set_title("Jumlah Pelanggan berdasarkan Negara Bagian")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Pelanggan berdasarkan Kota")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=customer_by_city.head(10), x='customer_city', y='count', palette=color_contrast, ax=ax)
        ax.set_xlabel("Kota")
        ax.set_ylabel("Jumlah Pelanggan")
        ax.set_title("10 Kota Teratas berdasarkan Jumlah Pelanggan")
        plt.xticks(rotation=45)
        st.pyplot(fig)

with tab3:    
    # Top 10 Products by Revenue and Quantity
    col1, col2 = st.columns([1, 1.1])
    with col1:
        st.subheader("10 Produk Teratas berdasarkan Revenue")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(data=top_10_products, x='product_category_name', y='revenue', palette=color_gradient, hue='revenue' ,legend=False, ax=ax)
        ax.set_xlabel("Kategori Produk")
        ax.set_ylabel("Total Revenue")
        ax.set_title("10 Produk Teratas berdasarkan Total Revenue")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        st.subheader("10 Produk Teratas berdasarkan Jumlah Terjual")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_10_products_quantity, x='product_category_name', y='order_item_id', palette=color_gradient, hue='order_item_id' ,ax=ax, legend=False)
        ax.set_xlabel("Kategori Produk")
        ax.set_ylabel("Total Jumlah Terjual")
        ax.set_title("10 Produk Teratas berdasarkan Total Jumlah Terjual")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Highest and Lowest Reviewed Products
    col1, col2 = st.columns([1.1, 1.05], gap='xxsmall')
    with col1:
        st.subheader("Produk dengan Ulasan Tertinggi")
        fig, ax = plt.subplots(figsize=(10, 6.25))
        sns.barplot(data=highest_reviewed_products, y='product_category_name', x='review_score', palette=color_gradient, hue='review_score' ,legend=False, ax=ax)
        ax.set_xlabel("Skor Ulasan Rata-rata")
        ax.set_ylabel("Kategori Produk")
        ax.set_title("10 Produk dengan Ulasan Tertinggi")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        st.subheader("Produk dengan Ulasan Terendah")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=lowest_reviewed_products, y='product_category_name', x='review_score', palette=red_gradient ,legend=False, ax=ax)
        ax.set_ylabel("Kategori Produk")
        ax.set_xlabel("Skor Ulasan Rata-rata")
        ax.set_title("10 Produk dengan Ulasan Terendah")
        plt.xticks(rotation=45)
        st.pyplot(fig)

with tab4:
    # Payment Type Distribution
    st.subheader("Distribusi Jenis Pembayaran")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=payment_type_distribution, y='payment_type', x='count', palette=color_contrast, ax=ax)
    ax.set_xlabel("Jumlah")
    ax.set_ylabel("Jenis Pembayaran")
    ax.set_title("Distribusi Jenis Pembayaran")
    st.pyplot(fig)

with tab5:
    # Average Review Score by Delivery Status by last quartal
    st.subheader("Skor Ulasan Rata-rata berdasarkan Status Pengiriman pada Kuartal Terakhir")

    last_quartal_date = filtered_df['order_purchase_timestamp'].max() - pd.DateOffset(months=3)
    last_quartal_data = filtered_df[filtered_df['order_purchase_timestamp'] >= last_quartal_date]
    average_review_score_by_delivery_status_last_quartal = create_average_review_score_by_delivery_status(last_quartal_data)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=average_review_score_by_delivery_status_last_quartal, x='delivery_status', y='review_score', palette=['lightblue', 'lightcoral'], ax=ax)
    ax.set_xlabel("Status Pengiriman")
    ax.set_ylabel("Skor Ulasan Rata-rata")
    ax.set_title("Skor Ulasan Rata-rata berdasarkan Status Pengiriman (Kuartal Terakhir)")
    st.pyplot(fig)


    
st.divider()
st.caption("Sumber Data: [Dataset Publik E-commerce Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")
st.caption("Dibuat oleh: **Andika Bagus Saputra** © 2026")