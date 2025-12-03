# Deployment Guide - NexSupply Platform

## Pre-Deployment Checklist

✅ **Completed:**
- [x] Database file removed from repository
- [x] `.gitignore` verified (includes `.env`, `*.db`, `__pycache__`, `.venv/`)
- [x] `python-dotenv` in requirements.txt
- [x] Gemini model confirmed: `gemini-2.5-flash`
- [x] All secrets removed from code

## Deployment Steps

### 1. GitHub Repository Setup

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Ready for deployment"

# Create GitHub repository and push
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud Deployment

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select your repository and branch**
5. **Set main file**: `streamlit_app.py`
6. **Add secrets** (Settings → Secrets):

```
GEMINI_API_KEY = "your-gemini-api-key"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "465"
SMTP_USERNAME = "outreach@nexsupply.net"
SMTP_PASSWORD = "your-app-password"
SMTP_FROM_EMAIL = "outreach@nexsupply.net"
```

7. **Click "Deploy"**

### 3. Mobile Access

- Streamlit apps are **automatically mobile-responsive**
- Access via mobile browser at your Streamlit Cloud URL
- No additional configuration needed
- Works on iOS Safari, Android Chrome, etc.

### 4. Post-Deployment

- Test all features on mobile device
- Verify email service (if configured)
- Check analytics dashboard: `https://your-app.streamlit.app/analytics?admin=1`

## Troubleshooting

### Common Issues

1. **"API Key not found"**
   - Check Streamlit Cloud secrets are set correctly
   - Verify secret names match exactly (case-sensitive)

2. **Email not sending**
   - Verify SMTP credentials in secrets
   - Check Gmail app password is correct
   - Port 465 (SMTP_SSL) is recommended

3. **Database errors**
   - Database is created automatically on first run
   - No manual setup needed

## Production Notes

- **Database**: SQLite database is created automatically in Streamlit Cloud
- **Secrets**: Use Streamlit Cloud secrets, not `.env` file
- **Performance**: Gemini 2.5 Flash provides fast, cost-effective responses
- **Mobile**: Fully responsive, no PWA needed

