# 🔒 Secure Deployment Guide

## Google Cloud Service Account Credentials

### ⚠️ IMPORTANT SECURITY NOTICE

**Never commit your actual credentials file to git!** The credentials file contains sensitive private keys that should be kept secure.

### 🔧 Setting Up Credentials

#### 1. **For Local Development**

1. Download your Google Cloud Service Account credentials from Google Cloud Console
2. Rename the file to `phonic-goods-317118-1353ffa1774d.json`
3. Place it in the project root directory
4. The file is already in `.gitignore` and will not be tracked by git

#### 2. **For Production Deployment**

Choose one of these secure methods:

##### Option A: Environment Variables (Recommended)
```bash
# Set the entire JSON as an environment variable
export GOOGLE_APPLICATION_CREDENTIALS_JSON='{
  "type": "service_account",
  "project_id": "your-project-id",
  ...
}'
```

##### Option B: Separate Environment Variables
```bash
export GOOGLE_PROJECT_ID="your-project-id"
export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
export GOOGLE_CLIENT_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"
# ... other fields
```

##### Option C: Platform-Specific Secret Management

**Heroku:**
```bash
heroku config:set GOOGLE_APPLICATION_CREDENTIALS_JSON="$(cat your-credentials.json)"
```

**Railway:**
- Go to Variables tab in Railway dashboard
- Add `GOOGLE_APPLICATION_CREDENTIALS_JSON` with your JSON content

**Docker:**
```bash
# Using secret mounts (Docker Swarm/Kubernetes)
docker run -v /path/to/credentials.json:/app/credentials.json:ro your-app
```

### 🔧 Code Modifications for Production

If using environment variables, modify `config.py`:

```python
import os
import json
import tempfile

class ProductionConfig(Config):
    # ... other config
    
    @staticmethod
    def get_credentials_file():
        # Try to get credentials from environment variable
        creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if creds_json:
            # Create temporary file with credentials
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(creds_json)
                return f.name
        
        # Fallback to file-based credentials
        return os.environ.get('CREDENTIALS_FILE', 'phonic-goods-317118-1353ffa1774d.json')
```

### 🛡️ Security Best Practices

1. **Never commit credentials** to version control
2. **Use principle of least privilege** - give service accounts only necessary permissions
3. **Rotate credentials regularly** (every 90 days recommended)
4. **Monitor credential usage** in Google Cloud Console
5. **Use separate credentials** for development and production
6. **Enable audit logging** for credential access

### 🚨 What to Do If Credentials Are Exposed

1. **Immediately revoke** the compromised service account key in Google Cloud Console
2. **Create a new** service account key
3. **Update all deployments** with new credentials
4. **Review audit logs** for any unauthorized access
5. **Consider rotating** related secrets and API keys

### 🔍 Verifying Security

Run this command to ensure no credentials are in your git history:
```bash
git log --all --full-history -- "*.json" | grep -i "private_key\|service_account"
```

If this returns any results, your git history may still contain credentials and needs cleaning.

### 📋 Environment Variables Checklist

For production deployment, ensure these are set:

- [ ] `SECRET_KEY` - Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] `FLASK_ENV=production` - Set production mode
- [ ] `SPREADSHEET_ID` - Your Google Sheets ID
- [ ] `GOOGLE_APPLICATION_CREDENTIALS_JSON` - Service account credentials (JSON string)
- [ ] `REQUEST_TIMEOUT=30` - Appropriate timeout for production
- [ ] `MAX_WORKERS=2` - Conservative worker count for production
- [ ] `MIN_DELAY=1.0` and `MAX_DELAY=3.0` - Respectful rate limiting

### 🆘 Emergency Contacts

If you suspect a security breach:
1. Contact your organization's security team immediately
2. Revoke all potentially compromised credentials
3. Review and update all related access permissions