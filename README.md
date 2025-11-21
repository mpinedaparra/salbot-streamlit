# Panini Scraper Dashboard

A Streamlit dashboard for visualizing product data from the Panini scraper system with Supabase authentication.

## Features

- 🔐 **Supabase Authentication**: Secure login with email/password
- 📊 **Dashboard Overview**: Key metrics and visualizations
- 📦 **Product Catalog**: Searchable and filterable product listings
- 📈 **Analytics**: Charts and marketplace comparisons
- 📥 **Export**: Download product data as CSV

## Local Development

### Prerequisites

- Python 3.11+
- Supabase account with products table
- Environment variables configured

### Setup

1. Install dependencies:
```bash
cd streamlit_app
pip install -r requirements.txt
```

2. Create `.env` file:
```env
SUPABASE_URL=your-project-url.supabase.co
SUPABASE_KEY=your-anon-key
```

3. Run locally:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

Ensure your `streamlit_app/` directory is in a GitHub repository.

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app/app.py`
6. Click "Advanced settings" → "Secrets"
7. Add your secrets:
```toml
SUPABASE_URL = "your-project-url.supabase.co"
SUPABASE_KEY = "your-anon-key"
```
8. Click "Deploy"

Your app will be available at: `https://your-app-name.streamlit.app`

### Step 3: Configure Supabase Auth

1. Go to Supabase Dashboard → Authentication → Providers
2. Enable "Email" provider
3. Create admin user:
   - Go to Authentication → Users
   - Click "Invite user"
   - Enter email and temporary password
   - User will receive invitation email

## Project Structure

```
streamlit_app/
├── app.py                    # Main entry point with auth
├── pages/
│   ├── 1_📦_Products.py      # Product listing
│   └── 2_📊_Analytics.py     # Analytics and charts
├── utils/
│   ├── supabase_client.py    # Supabase connection
│   └── auth.py               # Authentication helpers
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── requirements.txt
└── README.md
```

## Usage

1. **Login**: Use your Supabase credentials
2. **Dashboard**: View overview statistics
3. **Products**: Search and filter products
4. **Analytics**: Explore charts and comparisons
5. **Logout**: Click logout button in sidebar

## Security

- Authentication handled by Supabase Auth
- Passwords securely hashed by Supabase
- HTTPS enforced on Streamlit Cloud
- API keys safe for client-side use (anon key)

## Support

For issues or questions, please contact the administrator.
