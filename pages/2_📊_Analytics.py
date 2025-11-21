"""
Analytics page - Charts and visualizations for product data.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import check_authentication
from utils.supabase_client import get_supabase_client
from utils.data_fetcher import fetch_all_products

# Check authentication
if not check_authentication():
    st.warning("Please login from the home page.")
    st.stop()

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

supabase = get_supabase_client()

st.title("📊 Analytics & Insights")

# Fetch products
try:
    # Fetch all products with pagination
    products_df = fetch_all_products()
    
    if len(products_df) == 0:
        st.warning("No products found in database.")
        st.stop()
    
    # Marketplace Analysis
    st.header("🏪 Marketplace Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Products per marketplace
        marketplace_counts = products_df['marketplace'].value_counts().reset_index()
        marketplace_counts.columns = ['Marketplace', 'Products']
        
        fig = px.bar(
            marketplace_counts,
            x='Marketplace',
            y='Products',
            title="Products per Marketplace",
            color='Products',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock status by marketplace
        if 'in_stock' in products_df.columns:
            stock_by_marketplace = products_df.groupby(['marketplace', 'in_stock']).size().reset_index(name='count')
            stock_by_marketplace['in_stock'] = stock_by_marketplace['in_stock'].map({True: 'In Stock', False: 'Out of Stock'})
            
            fig = px.bar(
                stock_by_marketplace,
                x='marketplace',
                y='count',
                color='in_stock',
                title="Stock Status by Marketplace",
                barmode='group',
                color_discrete_map={'In Stock': '#00D26A', 'Out of Stock': '#FF4B4B'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Price Analysis
    st.header("💰 Price Analysis")
    
    # Extract numeric prices
    if 'price' in products_df.columns:
        products_df['price_numeric'] = products_df['price'].str.replace('$', '').str.replace('.', '').str.replace(',', '').astype(float, errors='ignore')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price distribution
            fig = px.histogram(
                products_df,
                x='price_numeric',
                nbins=30,
                title="Price Distribution",
                labels={'price_numeric': 'Price (CLP)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average price by marketplace
            avg_price_by_marketplace = products_df.groupby('marketplace')['price_numeric'].mean().reset_index()
            avg_price_by_marketplace.columns = ['Marketplace', 'Average Price']
            
            fig = px.bar(
                avg_price_by_marketplace,
                x='Marketplace',
                y='Average Price',
                title="Average Price by Marketplace",
                color='Average Price',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Marketplace Comparison Table
    st.header("📋 Marketplace Comparison")
    
    comparison_data = []
    for marketplace in products_df['marketplace'].unique():
        marketplace_df = products_df[products_df['marketplace'] == marketplace]
        
        comparison_data.append({
            'Marketplace': marketplace,
            'Total Products': len(marketplace_df),
            'In Stock': marketplace_df['in_stock'].sum() if 'in_stock' in marketplace_df.columns else 0,
            'Avg Price': f"${marketplace_df['price_numeric'].mean():,.0f}" if 'price_numeric' in marketplace_df.columns else 'N/A',
            'Min Price': f"${marketplace_df['price_numeric'].min():,.0f}" if 'price_numeric' in marketplace_df.columns else 'N/A',
            'Max Price': f"${marketplace_df['price_numeric'].max():,.0f}" if 'price_numeric' in marketplace_df.columns else 'N/A'
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Summary statistics
    st.header("📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(products_df))
    
    with col2:
        st.metric("Total Marketplaces", products_df['marketplace'].nunique())
    
    with col3:
        if 'price_numeric' in products_df.columns:
            st.metric("Highest Price", f"${products_df['price_numeric'].max():,.0f}")
    
    with col4:
        if 'price_numeric' in products_df.columns:
            st.metric("Lowest Price", f"${products_df['price_numeric'].min():,.0f}")

except Exception as e:
    st.error(f"Error loading analytics: {str(e)}")
