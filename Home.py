import streamlit as st
import pandas as pd

# Adjust Layout
st.set_page_config(layout="wide", page_title="Ecommerce Data Analysis", page_icon=":shopping_cart:")

# Make centered title
st.markdown("<h1 style='text-align: center;'>Ecommerce Data Analysis</h1>", unsafe_allow_html=True)

# Add Image from the web (make sure it is working)
st.image("https://marketplace.canva.com/EAGkJu6RBag/1/0/1600w/canva-pink-and-white-minimalist-e-commerce-presentation-pUrMakjsI6U.jpg")

# Read Data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_df.csv")
    return df

df = load_data()

# Show Data
st.subheader("Data Overview")
st.dataframe(df.head())

# Data Description (Explanation of what each column means)
st.subheader("Data Description")

column_descriptions = {
    "customer_name": "The name of the customer who placed the order",
    "gender": "Gender of the customer (Male/Female)",
    "age": "Age of the customer at the time of purchase",
    "city": "City where the customer is located",
    "state": "State/Territory where the customer is located",
    "order_date": "Date when the customer placed the order",
    "delivery_date": "Date when the order was delivered to the customer",
    "sales_id": "Unique identifier for the sales transaction",
    "price_per_unit": "Cost of a single unit of the product (in currency)",
    "quantity": "Number of units purchased in the order",
    "total_price": "Total amount paid for the order (price_per_unit × quantity)",
    "product_type": "Category of the product (e.g., Shirt, Jacket)",
    "product_name": "Specific name/style of the product",
    "size": "Size of the product (XS, S, M, L, XL, etc.)",
    "colour": "Color of the product",
    "Stock": "Available inventory/stock quantity at the time of order",
    "delivery_days": "Number of days taken to deliver the order after it was placed"
}

for column, description in column_descriptions.items():
    st.write(f"**{column}**: {description}")