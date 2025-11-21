"""
Data fetching utilities for Streamlit app.
"""
from utils.supabase_client import get_supabase_client
import pandas as pd

def fetch_all_products():
    """
    Fetch all products from Supabase with pagination.
    Supabase has a default limit of 1000 rows per query.
    
    Returns:
        pandas.DataFrame: All products
    """
    supabase = get_supabase_client()
    all_products = []
    page_size = 1000
    offset = 0
    
    while True:
        # Fetch page with range
        response = supabase.table('products')\
            .select('*')\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        if not response.data:
            break
        
        all_products.extend(response.data)
        
        # If we got less than page_size, we're done
        if len(response.data) < page_size:
            break
        
        offset += page_size
    
    return pd.DataFrame(all_products)
