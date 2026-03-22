import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
import folium
sns.set_style("whitegrid")

# Load Data
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
    data['delivery_status'] = (data['order_delivered_customer_date'] <= data['order_estimated_delivery_date']).apply(lambda x: 'On Time' if x else 'Late')
    average_review_score_by_delivery_status = data.groupby('delivery_status')['review_score'].mean().reset_index()
    
    return average_review_score_by_delivery_status

main_df = pd.read_csv("Dashboard/main_df.csv")

customer_by_state = create_customer_by_state(main_df)
customer_by_city = create_customer_by_city(main_df)
total_revenue = create_sum_revenue(main_df)
avg_revenue_per_order = create_avg_revenue_per_order(main_df)
top_10_products = create_top_10_products_by_revenue(main_df)
top_10_products_quantity = create_top_10_products_by_quantity(main_df)
monthly_revenue_trend = create_monthly_revenue_trend(main_df)
payment_type_distribution = create_payment_type_distribution(main_df)
highest_reviewed_products = create_highest_reviewed_products(main_df)
lowest_reviewed_products = create_lowest_reviewed_products(main_df)
average_review_score_by_delivery_status = create_average_review_score_by_delivery_status(main_df)

# Header

col1, col2 = st.columns([1, 6.5])
with col1:
    st.image("Dashboard/olist_logo.png")
with col2:
    st.title("Dashboard Olist E-commerce")  

# Metic Cards
col1, col2, col3 = st.columns([0.75, 1.25, 1], gap="medium")
with col1:
    st.metric(label="Total Customers", value=f"{main_df['customer_id'].nunique():,}")
with col2:
    st.metric(label="Total Revenue", value=f"R$ {total_revenue:,.2f}")
with col3:
    st.metric(label="Avg Revenue per Order", value=f"R$ {avg_revenue_per_order:,.2f}")

# Charts
color_contrast = ["#184375", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5", "#9dc2d5"]
color_gradient = sns.color_palette("Blues", n_colors=10)
red_gradient = sns.color_palette("Reds_r", n_colors=10)

# Monthly Revenue Trend
st.subheader("Monthly Revenue Trend")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_revenue_trend, x='month', y='revenue', marker='o', ax=ax)
ax.set_ylim(0, monthly_revenue_trend['revenue'].max() * 1.1)
ax.set_xlabel("Month")
ax.set_ylabel("Total Revenue")
ax.set_title("Monthly Revenue Trend")
plt.xticks(rotation=45)
st.pyplot(fig)

# Customers by State and City
col1, col2 = st.columns(2)
with col1:
    st.subheader("Customers by State")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=customer_by_state.head(10), x='customer_state', y='count', palette=color_contrast, ax=ax)
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Number of Customers by State")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Customers by City")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=customer_by_city.head(10), x='customer_city', y='count', palette=color_contrast, ax=ax)
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Top 10 Cities by Number of Customers")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Top 10 Products by Revenue and Quantity
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Products by Revenue")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_products, x='product_category_name', y='revenue', palette=color_gradient, hue='revenue' ,legend=False, ax=ax)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Top 10 Products by Total Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    st.subheader("Top 10 Products by Quantity Sold")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_products_quantity, x='product_category_name', y='order_item_id', palette=color_gradient, hue='order_item_id' ,ax=ax, legend=False)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Quantity Sold")
    ax.set_title("Top 10 Products by Total Quantity Sold")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Payment Type Distribution
st.subheader("Payment Type Distribution")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=payment_type_distribution, y='payment_type', x='count', palette=color_contrast, ax=ax)
ax.set_xlabel("Count")
ax.set_ylabel("Payment Type")
ax.set_title("Distribution of Payment Types")
st.pyplot(fig)

# Highest and Lowest Reviewed Products
col1, col2 = st.columns([1.1, 1.05], gap='xxsmall')
with col1:
    st.subheader("Highest Reviewed Products")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=highest_reviewed_products, y='product_category_name', x='review_score', palette=color_gradient, hue='review_score' ,legend=False, ax=ax)
    ax.set_xlabel("Average Review Score")
    ax.set_ylabel("Product Category")
    ax.set_title("Top 10 Highest Reviewed Products")
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    st.subheader("Lowest Reviewed Products")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=lowest_reviewed_products, y='product_category_name', x='review_score', palette=red_gradient ,legend=False, ax=ax)
    ax.set_ylabel("Product Category")
    ax.set_xlabel("Average Review Score")
    ax.set_title("Top 10 Lowest Reviewed Products")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Average Review Score by Delivery Status
st.subheader("Average Review Score by Delivery Status")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=average_review_score_by_delivery_status, x='delivery_status', y='review_score', palette=['salmon', 'lightgreen'], ax=ax)
ax.set_xlabel("Delivery Status")
ax.set_ylabel("Average Review Score")
ax.set_title("Average Review Score by Delivery Status")
ax.set_ylim(0, 5)
st.pyplot(fig)

st.divider()
st.caption("Data Source: [Olist E-commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")
st.caption("Created by: **Andika Bagus Saputra** © 2026")
