# Streamlit Dashboard Deployment Guide

## Quick Start - Streamlit Cloud Deployment

### 1. Create Supabase Admin User

First, create an admin user in your Supabase project:

1. Go to https://supabase.com/dashboard
2. Select your project
3. Navigate to **Authentication** → **Users**
4. Click **Invite user**
5. Enter email: `admin@panini.com` (or your preferred email)
6. Set a secure password
7. Click **Invite**

### 2. Push to GitHub

```bash
cd /home/manuel/CascadeProjects/panini_scraper
git add streamlit_app/
git commit -m "Add Streamlit dashboard with Supabase Auth"
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. Visit https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click **"New app"**
4. Configure:
   - **Repository**: Select `panini_scraper`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/app.py`
   - **App URL**: Choose a custom name (e.g., `panini-dashboard`)

5. Click **"Advanced settings"**
6. In the **Secrets** section, paste:
   ```toml
   SUPABASE_URL = "https://your-project-id.supabase.co"
   SUPABASE_KEY = "your-anon-key-here"
   ```
   
   > **Where to find these values:**
   > - Go to Supabase Dashboard → Settings → API
   > - **URL**: Project URL
   > - **Key**: `anon` `public` key

7. Click **"Deploy!"**

### 4. Access Your Dashboard

Your dashboard will be available at:
```
https://panini-dashboard.streamlit.app
```

Login with the admin credentials you created in Step 1.

## Local Development (Optional)

### Setup

```bash
cd streamlit_app
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
```

### Run Locally

```bash
streamlit run app.py
```

Dashboard will open at http://localhost:8501

## Adding More Users

### Via Supabase Dashboard

1. Go to Supabase Dashboard → Authentication → Users
2. Click **"Invite user"**
3. Enter email and password
4. User can now login to the dashboard

### Via SQL (Advanced)

```sql
-- In Supabase SQL Editor
INSERT INTO auth.users (
    instance_id,
    id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    created_at,
    updated_at
)
VALUES (
    '00000000-0000-0000-0000-000000000000',
    gen_random_uuid(),
    'authenticated',
    'authenticated',
    'newuser@example.com',
    crypt('secure-password', gen_salt('bf')),
    now(),
    now(),
    now()
);
```

## Troubleshooting

### Login Issues

- Verify Supabase URL and Key in secrets
- Check user exists in Supabase Dashboard → Authentication → Users
- Ensure email is confirmed

### Data Not Loading

- Verify `products` table exists in Supabase
- Check Row Level Security (RLS) policies allow authenticated reads
- Test Supabase connection in SQL Editor

### Deployment Fails

- Check `requirements.txt` is in `streamlit_app/` directory
- Verify Python version compatibility (3.11+)
- Review deployment logs in Streamlit Cloud dashboard

## Features

- ✅ Supabase Authentication
- ✅ Dashboard Overview with metrics
- ✅ Product Catalog with search/filters
- ✅ Analytics with charts
- ✅ CSV Export
- ✅ Responsive design
- ✅ HTTPS/SSL (automatic on Streamlit Cloud)

## Next Steps

1. Customize theme in `.streamlit/config.toml`
2. Add more analytics pages
3. Configure email templates in Supabase
4. Set up custom domain (Streamlit Cloud Pro)
