"""
Products page - Searchable and filterable product listing.
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, get_current_user
from utils.supabase_client import get_supabase_client

# Check authentication
if not check_authentication():
    st.warning("Please login from the home page.")
    st.stop()

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

user = get_current_user()
supabase = get_supabase_client()

st.title("📦 Product Catalog")

# Fetch products
try:
    response = supabase.table('products').select('*').execute()
    products_df = pd.DataFrame(response.data)
    
    if len(products_df) == 0:
        st.warning("No products found in database.")
        st.stop()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marketplaces = ['All'] + sorted(products_df['marketplace'].unique().tolist())
        selected_marketplace = st.selectbox("Marketplace", marketplaces)
    
    with col2:
        stock_options = ['All', 'In Stock', 'Out of Stock']
        selected_stock = st.selectbox("Stock Status", stock_options)
    
    with col3:
        search_term = st.text_input("🔍 Search products", placeholder="Enter product name...")
    
    # Apply filters
    filtered_df = products_df.copy()
    
    if selected_marketplace != 'All':
        filtered_df = filtered_df[filtered_df['marketplace'] == selected_marketplace]
    
    if selected_stock == 'In Stock':
        filtered_df = filtered_df[filtered_df['in_stock'] == True]
    elif selected_stock == 'Out of Stock':
        filtered_df = filtered_df[filtered_df['in_stock'] == False]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False, na=False)
        ]
    
    # Display results
    st.markdown(f"**Showing {len(filtered_df)} of {len(products_df)} products**")
    
    # Product table
    display_columns = ['name', 'marketplace', 'price', 'in_stock', 'product_url', 'scraped_at']
    display_columns = [col for col in display_columns if col in filtered_df.columns]
    
    # Format the dataframe
    display_df = filtered_df[display_columns].copy()
    
    # Make URLs clickable
    if 'product_url' in display_df.columns:
        display_df['product_url'] = display_df['product_url'].apply(
            lambda x: f'<a href="{x}" target="_blank">View</a>' if pd.notna(x) else ''
        )
    
    # Rename columns for better display
    column_config = {
        'name': st.column_config.TextColumn('Product Name', width='large'),
        'marketplace': st.column_config.TextColumn('Marketplace', width='small'),
        'price': st.column_config.TextColumn('Price', width='small'),
        'in_stock': st.column_config.CheckboxColumn('In Stock', width='small'),
        'product_url': st.column_config.LinkColumn('Link', width='small'),
        'scraped_at': st.column_config.DatetimeColumn('Last Updated', width='medium')
    }
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )
    
    # Export button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="products.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.metric("Total Results", len(filtered_df))

except Exception as e:
    st.error(f"Error loading products: {str(e)}")
