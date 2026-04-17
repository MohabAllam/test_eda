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

# Add Numerical and Categorical Tabs
num_tab, cat_tab, custom_tab = st.tabs(["Numerical Analysis", "Categorical Analysis", 'Custom Analysis'])

# Numerical Columns
num_columns = df.select_dtypes(include=['number']).columns

# Numerical Analysis
with num_tab:
    st.subheader("Numerical Columns")
    for col in num_columns:
        st.write(f"**{col}**")
        st.plotly_chart(px.histogram(df, x=col, title=f"Distribution of {col}"))

# Categorical Analysis
cat_columns = df.select_dtypes(include=['object']).columns
with cat_tab:
    st.subheader("Categorical Columns")
    for col in cat_columns:
        st.write(f"**{col}**")
        st.plotly_chart(px.histogram(df, x=col, title=f"Distribution of {col}").update_xaxes(categoryorder='max descending'))

# Custom Analysis
with custom_tab:
    st.subheader("Custom Analysis")
    col1, col2, = st.columns(2)
    with col1:
        col1 = st.selectbox("Select Column", options=df.columns)
    with col2:
        col2 = st.selectbox("Select Chart Type", options=["Histogram", "Pie Chart"])

    # Add button to generate chart
    if st.button("Generate Chart"): 

        if col2 == "Histogram":
            st.plotly_chart(px.histogram(df, x=col1))
        elif col2 == "Pie Chart":
            st.plotly_chart(px.pie(df, names=col1, title=f"Distribution of {col1}"))    

