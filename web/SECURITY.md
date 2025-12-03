# 🔒 NexSupply Security Guide

## API Keys & Secrets Management

### Required Secrets

NexSupply requires the following secrets to function:

1. **GEMINI_API_KEY** - Google Gemini API key for AI analysis
2. **SMTP credentials** - For email service (optional, for consultation requests)

### Setup Instructions

1. **Copy the example file:**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Fill in your actual secrets:**
   - Open `.streamlit/secrets.toml`
   - Replace placeholder values with your actual API keys
   - **NEVER commit this file to Git**

3. **Verify .gitignore:**
   - Ensure `.streamlit/secrets.toml` is in `.gitignore`
   - The example file (`.secrets.toml.example`) is safe to commit

### Environment Variables (Alternative)

You can also use environment variables instead of `secrets.toml`:

```bash
export GEMINI_API_KEY="your-key-here"
export SMTP_USERNAME="your-email@example.com"
export SMTP_PASSWORD="your-password"
```

### Production Deployment

For production environments:

1. **Use a Secret Management Service:**
   - AWS Secrets Manager
   - Google Secret Manager
   - Azure Key Vault

2. **Never hardcode secrets in:**
   - Source code files
   - Configuration files committed to Git
   - Public repositories

3. **Rotate keys regularly:**
   - Change API keys every 90 days
   - Revoke compromised keys immediately

## Error Handling & Security

### Error Messages

- All error messages use generic error codes (e.g., `A-101`, `E-201`)
- Internal technical details are never exposed to users
- All errors are logged internally for debugging

### Logging

- Production logging level: `WARNING` (errors and warnings only)
- No sensitive data in logs
- All print() statements replaced with proper logging

## Data Privacy

### User Data

- Email addresses are encrypted in transit (HTTPS)
- Analysis data is stored locally (SQLite) for analytics
- Users can request data deletion

### Contact Information

- Public email: `outreach@nexsupply.net` (safe to expose)
- Internal admin emails: Use environment variables

## Intellectual Property Protection

### Core Logic

- Cost calculation formulas are in `utils/cost_calculator.py`
- Risk assessment logic is proprietary
- Prompt templates are in `utils/prompts.py`

### Protection Measures

- Core logic is server-side only
- No client-side exposure of calculation methods
- Proprietary algorithms are not documented in public code

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email: **security@nexsupply.net** (or outreach@nexsupply.net)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact

## Compliance

- **Terms of Service**: See `/legal` page
- **Privacy Policy**: See `/legal` page
- **GDPR**: User data deletion available on request

---

*Last updated: November 2024*

