"""
Main Streamlit application - Home page with authentication and overview.
"""
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from utils.auth import check_authentication, login_form, logout, get_current_user, send_password_reset
from utils.supabase_client import get_supabase_client
from utils.data_fetcher import fetch_all_products

# Load environment variables (for local development)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Panini Scraper Dashboard",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if not check_authentication():
    login_form()
    st.stop()

# User is authenticated - show dashboard
user = get_current_user()
supabase = get_supabase_client()

# Sidebar
with st.sidebar:
    st.title("🎴 Panini Dashboard")
    st.markdown("---")
    st.write(f"👤 **User:** {user.email}")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
    
    st.markdown("---")
    st.markdown("### Navigation")
    st.info("Use the pages in the sidebar to explore products and analytics.")

# Main content
st.title("📊 Dashboard Overview")

# Fetch data
try:
    # Fetch all products with pagination
    products_df = fetch_all_products()
    
    if len(products_df) == 0:
        st.warning("No products found in database.")
        st.stop()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Products",
            value=len(products_df)
        )
    
    with col2:
        in_stock = products_df['in_stock'].sum() if 'in_stock' in products_df.columns else 0
        st.metric(
            label="In Stock",
            value=int(in_stock)
        )
    
    with col3:
        marketplaces = products_df['marketplace'].nunique() if 'marketplace' in products_df.columns else 0
        st.metric(
            label="Marketplaces",
            value=marketplaces
        )
    
    with col4:
        avg_price = products_df['price'].str.replace('$', '').str.replace('.', '').astype(float).mean() if 'price' in products_df.columns else 0
        st.metric(
            label="Avg Price",
            value=f"${avg_price:,.0f}"
        )
    
    st.markdown("---")
    
    # Products by marketplace
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Products by Marketplace")
        if 'marketplace' in products_df.columns:
            marketplace_counts = products_df['marketplace'].value_counts().reset_index()
            marketplace_counts.columns = ['Marketplace', 'Count']
            
            fig = px.bar(
                marketplace_counts,
                x='Marketplace',
                y='Count',
                color='Marketplace',
                title="Product Distribution"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Stock Status")
        if 'in_stock' in products_df.columns:
            stock_counts = products_df['in_stock'].value_counts().reset_index()
            stock_counts.columns = ['Status', 'Count']
            stock_counts['Status'] = stock_counts['Status'].map({True: 'In Stock', False: 'Out of Stock'})
            
            fig = px.pie(
                stock_counts,
                values='Count',
                names='Status',
                title="Stock Distribution",
                color='Status',
                color_discrete_map={'In Stock': '#00D26A', 'Out of Stock': '#FF4B4B'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent products
    st.subheader("🆕 Recently Updated Products")
    if 'scraped_at' in products_df.columns:
        recent_products = products_df.sort_values('scraped_at', ascending=False).head(10)
        display_cols = ['name', 'marketplace', 'price', 'in_stock', 'scraped_at']
        display_cols = [col for col in display_cols if col in recent_products.columns]
        st.dataframe(
            recent_products[display_cols],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No timestamp information available.")

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please check your Supabase connection and ensure the products table exists.")
