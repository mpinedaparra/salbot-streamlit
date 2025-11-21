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
    
    # Forgot password section
    st.markdown("---")
    with st.expander("🔐 Forgot Password?"):
        st.write("Enter your email to receive a password reset link.")
        reset_email = st.text_input("Email", key="reset_email", placeholder="your@email.com")
        
        if st.button("Send Reset Link", use_container_width=True):
            if not reset_email:
                st.error("Please enter your email address.")
            else:
                if send_password_reset(reset_email):
                    st.success("✅ Password reset email sent! Check your inbox.")
                    st.info("The link will expire in 1 hour.")
                else:
                    st.error("Failed to send reset email. Please try again.")

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

def send_password_reset(email):
    """
    Send password reset email to user.
    
    Args:
        email: User's email address
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        supabase = get_supabase_client()
        # Supabase will send reset email with link to your app
        supabase.auth.reset_password_for_email(
            email,
            options={
                "redirect_to": "https://salbot-app-z6okgwwbpkyd9nufqccdmn.streamlit.app/Reset_Password"
            }
        )
        return True
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return False
