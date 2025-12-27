import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# DB Connection
DB_URL = "postgresql+psycopg2://postgres:mypassword123@localhost:5432/sales_db"  # Update password
engine = create_engine(DB_URL)

st.title("🛒 Universal Sales Analytics Dashboard for Consumer Durables")
st.markdown("Analyze sales performance, campaigns, customer retention, and more.")

# Load data
@st.cache_data
def load_data():
    sales_df = pd.read_sql("SELECT * FROM sales_data", engine)
    cohorts_df = pd.read_sql("SELECT * FROM customer_cohorts", engine)
    return sales_df, cohorts_df

sales_df, cohorts_df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
product_filter = st.sidebar.multiselect("Product", options=sales_df['product'].unique())
geo_filter = st.sidebar.multiselect("Geography", options=sales_df['geography'].unique())

filtered_df = sales_df
if product_filter:
    filtered_df = filtered_df[filtered_df['product'].isin(product_filter)]
if geo_filter:
    filtered_df = filtered_df[filtered_df['geography'].isin(geo_filter)]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered_df['total_amount'].sum()
total_orders = len(filtered_df)
avg_ticket = filtered_df['total_amount'].mean()
repeat_rate = (filtered_df['is_repeat'].sum() / len(filtered_df)) * 100

with col1:
    st.metric("Total Sales", f"₹{total_sales:,.2f}")
with col2:
    st.metric("Total Orders", total_orders)
with col3:
    st.metric("Avg Ticket Size", f"₹{avg_ticket:,.2f}")
with col4:
    st.metric("Repeat Rate", f"{repeat_rate:.1f}%")

# Sales Performance Chart
fig1 = px.bar(filtered_df.groupby(['product', 'geography'])['total_amount'].sum().reset_index(),
              x='product', y='total_amount', color='geography', title="Sales by Product & Geography")
st.plotly_chart(fig1)

# Campaign ROI (Simple: Sales by Campaign)
campaign_sales = filtered_df.groupby('campaign_id')['total_amount'].agg(['sum', 'count']).reset_index()
campaign_sales['roi_proxy'] = campaign_sales['sum'] / campaign_sales['count']  # Proxy for ROI
fig2 = px.bar(campaign_sales, x='campaign_id', y='roi_proxy', title="Campaign Effectiveness (Avg Sales per Order)")
st.plotly_chart(fig2)

# Customer Cohorts & Churn
st.subheader("Customer Retention Insights")
churn_fig = px.histogram(cohorts_df, x='churn_days', color='segment', title="Churn Distribution by Segment")
st.plotly_chart(churn_fig)

cohort_retention = cohorts_df.groupby('segment')['total_purchases'].mean().reset_index()
fig3 = px.pie(cohort_retention, values='total_purchases', names='segment', title="Avg Purchases by Segment")
st.plotly_chart(fig3)

# Raw Data Table
st.subheader("Sales Data Table")
st.dataframe(filtered_df)

# Insights Section (Automated)
st.subheader("Key Insights")
if repeat_rate > 25:
    st.success("High repeat purchase rate – Focus on loyalty programs!")
else:
    st.warning("Low repeat rate – Analyze churn drivers.")