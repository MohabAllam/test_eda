import streamlit as st
import pandas as pd
import plotly.express as px

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

# Convert date columns to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
df['delivery_date'] = pd.to_datetime(df['delivery_date'])

st.subheader("Bivariate & Multivariate Analysis")

# 1. Age & Total Price by Gender
st.markdown("### 1. How does customer age influence purchase value across genders?")
fig1 = px.scatter(df, x='age', y='total_price', color='gender', title='Age vs Total Price by Gender',
                   labels={'age': 'Customer Age', 'total_price': 'Total Price'},
                   trendline='ols', hover_data=['product_type', 'quantity'])
st.plotly_chart(fig1, use_container_width=True)

age_gender_analysis = df.groupby('gender').agg({'age': 'mean', 'total_price': 'mean', 'quantity': 'mean'}).round(2)
st.write("**Pandas Analysis:**")
st.dataframe(age_gender_analysis)

# 2. Product Type Sales by Gender
st.markdown("### 2. What are the product type preferences across different genders?")
product_gender = df.groupby(['gender', 'product_type']).size().reset_index(name='count')
fig2 = px.bar(product_gender, x='product_type', y='count', color='gender', barmode='group',
              title='Product Type Preferences by Gender', labels={'count': 'Number of Orders'})
st.plotly_chart(fig2, use_container_width=True)

product_stats = df.groupby(['gender', 'product_type']).agg({'total_price': 'mean', 'quantity': 'mean'}).round(2)
st.write("**Pandas Analysis:**")
st.dataframe(product_stats)

# 3. Delivery Days vs Total Price
st.markdown("### 3. How does delivery time affect product pricing strategy?")
delivery_by_product = df.groupby('product_type').agg({'delivery_days': 'mean', 'price_per_unit': 'mean'}).reset_index()
fig3 = px.bar(delivery_by_product, x='product_type', y='delivery_days', title='Average Delivery Days by Product Type',
              labels={'product_type': 'Product Type', 'delivery_days': 'Average Delivery Days'},
              color='delivery_days', color_continuous_scale='Blues')
st.plotly_chart(fig3, use_container_width=True)

delivery_analysis = df.groupby('product_type').agg({'delivery_days': 'mean', 'price_per_unit': 'mean'}).round(2)
st.write("**Pandas Analysis:**")
st.dataframe(delivery_analysis)

# 4. State-wise Average Order Value & Volume
st.markdown("### 4. Which states generate the highest order values and volumes?")
state_analysis = df.groupby('state').agg({'total_price': ['sum', 'mean', 'count']}).round(2)
state_analysis.columns = ['Total Revenue', 'Average Order Value', 'Order Count']
state_analysis = state_analysis.sort_values('Total Revenue', ascending=False).head(10)

fig4 = px.bar(state_analysis.reset_index(), x='state', y='Total Revenue', 
              title='Top 10 States by Total Revenue', labels={'state': 'State', 'Total Revenue': 'Revenue'})
st.plotly_chart(fig4, use_container_width=True)

st.write("**Pandas Analysis:**")
st.dataframe(state_analysis)

# 5. Quantity vs Total Price by Product Type
st.markdown("### 5. How does purchase quantity influence total spending by product category?")
price_by_product = df.groupby('product_type').agg({'total_price': 'mean'}).reset_index()
fig5 = px.bar(price_by_product, x='product_type', y='total_price', title='Average Total Price by Product Type',
              labels={'product_type': 'Product Type', 'total_price': 'Average Total Price'},
              color='total_price', color_continuous_scale='Greens')
st.plotly_chart(fig5, use_container_width=True)

qty_analysis = df.groupby('product_type').agg({'quantity': 'mean', 'total_price': ['mean', 'median', 'std']}).round(2)
st.write("**Pandas Analysis:**")
st.dataframe(qty_analysis)

# 6. Size Distribution by Gender
st.markdown("### 6. What size preferences differ between male and female customers?")
size_gender = df.groupby(['gender', 'size']).size().reset_index(name='count').sort_values('count', ascending=False).head(8)
fig6 = px.bar(size_gender, x='size', y='count', color='gender', barmode='group',
              title='Top Size Preferences by Gender',
              labels={'size': 'Size', 'count': 'Number of Orders'})
st.plotly_chart(fig6, use_container_width=True)

size_stats = df.groupby(['gender', 'size']).size().unstack(fill_value=0)
st.write("**Pandas Analysis:**")
st.dataframe(size_stats)

# 7. Color Preferences by Age Group
st.markdown("### 7. How do color preferences vary across different age groups?")
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 100], labels=['18-25', '26-35', '36-45', '45+'])
color_age = df.groupby(['age_group', 'colour']).size().reset_index(name='count').sort_values('count', ascending=False).head(15)

fig7 = px.bar(color_age, x='age_group', y='count', color='colour', barmode='stack',
              title='Top Color Preferences by Age Group',
              labels={'age_group': 'Age Group', 'count': 'Number of Orders'})
st.plotly_chart(fig7, use_container_width=True)

color_stats = df.groupby(['age_group', 'colour']).size().unstack(fill_value=0).iloc[:, :5]
st.write("**Pandas Analysis:**")
st.dataframe(color_stats)

# 8. Order Trends by Product Type Over Time
st.markdown("### 8. How do order volumes and values trend over time for different product types?")
df['month'] = df['order_date'].dt.to_period('M').astype(str)
monthly_product = df.groupby(['month', 'product_type']).agg({'total_price': 'sum', 'sales_id': 'count'}).reset_index()
monthly_product.columns = ['month', 'product_type', 'total_revenue', 'order_count']

fig8 = px.line(monthly_product, x='month', y='total_revenue', color='product_type',
               title='Monthly Revenue Trends by Product Type',
               labels={'month': 'Month', 'total_revenue': 'Total Revenue'})
st.plotly_chart(fig8, use_container_width=True)

trend_analysis = df.groupby('product_type').agg({'sales_id': 'count', 'total_price': 'sum'}).round(0)
st.write("**Pandas Analysis:**")
st.dataframe(trend_analysis)

# 9. Stock Levels vs Price Per Unit
st.markdown("### 9. Is there a relationship between stock availability and product pricing?")
stock_by_product = df.groupby('product_type').agg({'Stock': 'mean', 'price_per_unit': 'mean'}).reset_index()
fig9 = px.bar(stock_by_product, x='product_type', y='Stock', title='Average Stock Level by Product Type',
              labels={'product_type': 'Product Type', 'Stock': 'Average Stock Level'},
              color='Stock', color_continuous_scale='Oranges')
st.plotly_chart(fig9, use_container_width=True)

stock_analysis = df.groupby('product_type').agg({'Stock': ['mean', 'min', 'max'], 'price_per_unit': 'mean'}).round(2)
st.write("**Pandas Analysis:**")
st.dataframe(stock_analysis)

# 10. Top Customers by Total Spending
st.markdown("### 10. Which customer segments contribute the most to revenue?")
customer_analysis = df.groupby('customer_name').agg({
    'total_price': 'sum',
    'sales_id': 'count',
    'age': 'first',
    'gender': 'first'
}).reset_index()
customer_analysis.columns = ['Customer Name', 'Total Spent', 'Order Count', 'Age', 'Gender']
customer_analysis = customer_analysis.sort_values('Total Spent', ascending=False).head(15)

fig10 = px.bar(customer_analysis, x='Customer Name', y='Total Spent', color='Gender',
               title='Top 15 Customers by Total Spending',
               labels={'Customer Name': 'Customer', 'Total Spent': 'Total Revenue'})
st.plotly_chart(fig10, use_container_width=True)

st.write("**Pandas Analysis:**")
st.dataframe(customer_analysis)