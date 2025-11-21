"""
Password Reset page - Handles password reset token from Supabase.
This page is accessed when user clicks the reset link in their email.
"""
import streamlit as st
from utils.supabase_client import get_supabase_client
import urllib.parse

st.set_page_config(page_title="Reset Password", page_icon="🔐", layout="centered")

st.title("🔐 Reset Password")

# Get query parameters from URL
query_params = st.query_params

# Check if we have a reset token
if "access_token" in query_params or "token" in query_params:
    token = query_params.get("access_token") or query_params.get("token")
    
    st.info("Please enter your new password below.")
    
    with st.form("reset_password_form"):
        new_password = st.text_input("New Password", type="password", help="Minimum 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Reset Password", use_container_width=True)
        
        if submit:
            # Validate passwords
            if not new_password or not confirm_password:
                st.error("Please fill in both password fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                try:
                    supabase = get_supabase_client()
                    
                    # Update password using the token
                    response = supabase.auth.update_user({
                        "password": new_password
                    })
                    
                    if response:
                        st.success("✅ Password reset successful!")
                        st.info("You can now login with your new password.")
                        
                        # Provide link to home page
                        st.markdown("---")
                        if st.button("Go to Login", use_container_width=True):
                            st.switch_page("app.py")
                    else:
                        st.error("Failed to reset password. Please try again.")
                        
                except Exception as e:
                    st.error(f"Error resetting password: {str(e)}")
                    st.info("The reset link may have expired. Please request a new one.")

else:
    # No token in URL - show message
    st.warning("No reset token found.")
    st.info("This page is accessed via the password reset link sent to your email.")
    
    st.markdown("---")
    st.markdown("### Need to reset your password?")
    st.markdown("1. Go to the login page")
    st.markdown("2. Click on 'Forgot Password?'")
    st.markdown("3. Enter your email")
    st.markdown("4. Check your email for the reset link")
    
    if st.button("Go to Login", use_container_width=True):
        st.switch_page("app.py")
