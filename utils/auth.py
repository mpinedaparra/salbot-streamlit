"""
Authentication utilities for Streamlit app using Supabase Auth.
"""
import streamlit as st
from utils.supabase_client import get_supabase_client

def check_authentication():
    """
    Check if user is authenticated. If not, show login form.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    if 'user' in st.session_state and st.session_state.user is not None:
        return True
    return False

def login_form():
    """
    Display login form and handle authentication.
    """
    st.title("🎴 Panini Scraper Dashboard")
    st.markdown("---")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="admin@example.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
                return
            
            try:
                supabase = get_supabase_client()
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    st.session_state.user = auth_response.user
                    st.session_state.session = auth_response.session
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Login failed. Please check your credentials.")
                    
            except Exception as e:
                st.error(f"Login error: {str(e)}")

def logout():
    """
    Logout current user and clear session.
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except:
        pass
    
    # Clear session state
    if 'user' in st.session_state:
        del st.session_state.user
    if 'session' in st.session_state:
        del st.session_state.session
    
    st.rerun()

def get_current_user():
    """
    Get current authenticated user.
    
    Returns:
        User object or None
    """
    return st.session_state.get('user', None)
