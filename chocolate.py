import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load the data
df = pd.read_csv("Cleaned_Chocolate_Sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
country = st.sidebar.selectbox("🌍 Select Country", options=["All"] + list(df["Country"].unique()))
product = st.sidebar.selectbox("🍫 Select Product", options=["All"] + list(df["Product"].unique()))
date_range = st.sidebar.date_input("📅 Date Range", [df["Date"].min(), df["Date"].max()])

# Apply filters
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if product != "All":
    filtered_df = filtered_df[filtered_df["Product"] == product]
filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(date_range[0])) & 
    (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
]

# Metrics
total_sales = filtered_df["Amount"].sum()
total_boxes = filtered_df["Boxes Shipped"].sum()
total_orders = filtered_df.shape[0]

st.title("🍫 Chocolate Sales Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📦 Total Boxes", f"{total_boxes}")
col3.metric("🧾 Orders", f"{total_orders}")

st.markdown("---")

# Sales Over Time
st.subheader("📈 Sales Over Time")
sales_over_time = filtered_df.groupby("Date")["Amount"].sum().reset_index()
line_chart = alt.Chart(sales_over_time).mark_area(opacity=0.5).encode(
    x="Date:T",
    y="Amount:Q",
    tooltip=["Date", "Amount"]
).properties(width=900, height=400)
st.altair_chart(line_chart, use_container_width=True)

# Sales by Country
st.subheader("🌍 Sales by Country")
sales_country = filtered_df.groupby("Country")["Amount"].sum().reset_index()
fig1 = px.bar(sales_country, x="Country", y="Amount", color="Country", title="Total Sales by Country")
st.plotly_chart(fig1, use_container_width=True)

# Top Products
st.subheader("🍫 Top Selling Products")
top_products = filtered_df.groupby("Product")["Amount"].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top_products, x="Amount", y="Product", orientation='h', title="Top 10 Products", color="Amount")
st.plotly_chart(fig2, use_container_width=True)

# Bubble Chart: Product vs Boxes vs Amount
st.subheader("🫧 Product Performance")
bubble_df = filtered_df.groupby("Product")[["Amount", "Boxes Shipped"]].sum().reset_index()
fig3 = px.scatter(bubble_df, x="Boxes Shipped", y="Amount", size="Amount", color="Product", title="Boxes vs Amount by Product", hover_name="Product")
st.plotly_chart(fig3, use_container_width=True)
