"""
Products page - Searchable and filterable product listing.
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, get_current_user
from utils.supabase_client import get_supabase_client
from utils.data_fetcher import fetch_all_products

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
    # Fetch all products with pagination
    products_df = fetch_all_products()
    
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
        search_term = st.text_input("🔍 Search products", placeholder="e.g., Patrulla guerra")
    
    # Apply filters
    filtered_df = products_df.copy()
    
    if selected_marketplace != 'All':
        filtered_df = filtered_df[filtered_df['marketplace'] == selected_marketplace]
    
    if selected_stock == 'In Stock':
        filtered_df = filtered_df[filtered_df['in_stock'] == True]
    elif selected_stock == 'Out of Stock':
        filtered_df = filtered_df[filtered_df['in_stock'] == False]
    
    # Multi-word search: all words must be present (AND logic)
    if search_term:
        # Split search term into words
        search_words = search_term.lower().split()
        
        # Filter: all words must be present in the product name
        def matches_all_words(name):
            if pd.isna(name):
                return False
            name_lower = name.lower()
            return all(word in name_lower for word in search_words)
        
        filtered_df = filtered_df[filtered_df['name'].apply(matches_all_words)]
    
    # Display results
    st.markdown(f"**Showing {len(filtered_df)} of {len(products_df)} products**")
    
    # Prepare data for display
    display_df = filtered_df.copy()
    
    # Add numeric price column for sorting (ignore decimals after comma)
    if 'price' in display_df.columns:
        def parse_price(price_str):
            """
            Parse price string to integer, removing formatting and decimals.
            Examples:
                $148.900,00 -> 148900
                $12.990 -> 12990
                $7.490 -> 7490
            """
            if pd.isna(price_str):
                return 0
            
            # Convert to string and remove $
            price_str = str(price_str).replace('$', '').strip()
            
            # Split by comma to remove decimals (,00)
            if ',' in price_str:
                price_str = price_str.split(',')[0]
            
            # Remove dots (thousands separator)
            price_str = price_str.replace('.', '')
            
            # Convert to int
            try:
                return int(price_str)
            except:
                return 0
        
        display_df['price_numeric'] = display_df['price'].apply(parse_price)
        # Sort by price numeric by default
        display_df = display_df.sort_values('price_numeric', ascending=True)
    
    # Select columns to display
    display_columns = ['image_url', 'name', 'marketplace', 'price', 'in_stock', 'product_url', 'scraped_at']
    display_columns = [col for col in display_columns if col in display_df.columns]
    
    # Column configuration with proper types
    column_config = {
        'image_url': st.column_config.ImageColumn(
            'Image',
            width='small',
            help="Product image"
        ),
        'name': st.column_config.TextColumn(
            'Product Name',
            width='large',
            help="Product name"
        ),
        'marketplace': st.column_config.TextColumn(
            'Marketplace',
            width='small'
        ),
        'price': st.column_config.NumberColumn(
            'Price',
            width='small',
            format="$%d",
            help="Price in CLP (sorted numerically)"
        ),
        'in_stock': st.column_config.CheckboxColumn(
            'In Stock',
            width='small'
        ),
        'product_url': st.column_config.LinkColumn(
            'Link',
            width='small',
            display_text="View"
        ),
        'scraped_at': st.column_config.DatetimeColumn(
            'Last Updated',
            width='medium',
            format="DD/MM/YY HH:mm"
        )
    }
    
    # Replace price string with numeric for display
    if 'price' in display_df.columns and 'price_numeric' in display_df.columns:
        display_df['price'] = display_df['price_numeric']
    
    # Remove price_numeric from display
    final_display_cols = [col for col in display_columns if col != 'price_numeric']
    
    st.dataframe(
        display_df[final_display_cols],
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
