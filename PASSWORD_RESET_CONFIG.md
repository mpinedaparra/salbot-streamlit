# Password Reset Configuration for Streamlit Cloud

## Important: Update Redirect URL

Before deploying, you need to update the redirect URL in the code to match your Streamlit app URL.

### Step 1: Update `utils/auth.py`

Find this line in `send_password_reset()` function:

```python
"redirect_to": "https://your-app.streamlit.app/Reset_Password"
```

Replace `your-app.streamlit.app` with your actual Streamlit Cloud URL.

**Example:**
```python
"redirect_to": "https://panini-dashboard.streamlit.app/Reset_Password"
```

### Step 2: Configure Supabase URL Configuration

1. Go to Supabase Dashboard → Authentication → URL Configuration
2. Add your reset password page URL to **Redirect URLs**:
   - `https://your-app.streamlit.app/Reset_Password`
   - `https://your-app.streamlit.app/**` (wildcard for all pages)

### Step 3: Test the Flow

1. **Request Reset:**
   - Go to login page
   - Click "Forgot Password?"
   - Enter email
   - Click "Send Reset Link"

2. **Check Email:**
   - Open email inbox
   - Find "Reset Password" email from Supabase
   - Click the reset link

3. **Reset Password:**
   - You'll be redirected to `/Reset_Password` page
   - Enter new password (min 6 characters)
   - Confirm password
   - Click "Reset Password"

4. **Login:**
   - Return to home page
   - Login with new password

## Troubleshooting

### "No reset token found"
- Check that Supabase redirect URL is configured correctly
- Verify the link hasn't expired (1 hour limit)
- Request a new reset link

### "Failed to send reset email"
- Verify email exists in Supabase
- Check Supabase email rate limits (3/hour on free tier)
- Check Supabase logs for errors

### "Error resetting password"
- Token may have expired
- Request a new reset link
- Check browser console for errors

## Files Modified

1. `pages/9_🔐_Reset_Password.py` - New page to handle reset token
2. `utils/auth.py` - Added `send_password_reset()` function and forgot password UI
3. `app.py` - Updated imports

## Next Steps

1. Update redirect URL in `utils/auth.py`
2. Configure Supabase redirect URLs
3. Deploy to Streamlit Cloud
4. Test complete flow
