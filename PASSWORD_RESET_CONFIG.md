# Password Reset - Simplified Approach

## How It Works

We're using Supabase's **built-in password reset page** instead of a custom Streamlit page. This is simpler and more reliable.

## User Flow

1. **User requests reset:**
   - Goes to login page
   - Clicks "Forgot Password?"
   - Enters email
   - Clicks "Send Reset Link"

2. **User receives email:**
   - Email contains reset link
   - Link goes to Supabase's hosted reset page

3. **User resets password:**
   - Clicks link in email
   - Supabase shows password reset form
   - User enters new password
   - Supabase confirms reset

4. **User returns to app:**
   - Can now login with new password

## Why This Approach?

**Problem with custom page:**
- Supabase sends token as hash fragment (`#access_token=...`)
- Streamlit can't read hash fragments server-side
- Would require complex JavaScript workarounds

**Benefits of Supabase page:**
- ✅ Works out of the box
- ✅ No custom code needed
- ✅ Secure and maintained by Supabase
- ✅ Mobile-friendly
- ✅ Handles token expiration automatically

## Customization (Optional)

You can customize the Supabase reset page:

1. Go to Supabase Dashboard → Authentication → Email Templates
2. Click "Reset Password"
3. Customize the email template
4. The reset page itself can be styled via Supabase settings

## Testing

1. Go to your dashboard login
2. Click "Forgot Password?"
3. Enter your email
4. Check inbox for reset email
5. Click link → Supabase page opens
6. Enter new password
7. Return to dashboard and login

## Files Modified

- `utils/auth.py` - Simplified `send_password_reset()` function
- Removed `pages/9_🔐_Reset_Password.py` (no longer needed)

## Next Steps

1. Push changes to GitHub
2. Streamlit Cloud will redeploy
3. Test the forgot password flow
4. Users can now reset passwords easily
