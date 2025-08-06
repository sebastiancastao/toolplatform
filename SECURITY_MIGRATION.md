# 🔐 Security Migration Guide

## Migration from JSON Credentials to Environment Variables

This guide explains the recent security improvements implemented to replace JSON credential files with environment variables.

## ✅ What Changed

### Before (Security Risk)
- Google Cloud credentials stored in JSON files
- Credential files potentially committed to version control
- Harder to manage different credentials across environments

### After (Secure)
- All credentials moved to environment variables
- No credential files in the codebase
- Easy environment-specific configuration
- Better security practices

## 🚀 Migration Steps

### 1. Environment Variables Setup

Copy these variables to your `.env` file or environment configuration:

```bash
# Google Cloud Service Account Configuration
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_PRIVATE_KEY_ID=your-private-key-id
GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
GOOGLE_CLOUD_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_CLIENT_ID=your-client-id
GOOGLE_CLOUD_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_CLOUD_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLOUD_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_UNIVERSE_DOMAIN=googleapis.com

# Google Sheets Configuration
SPREADSHEET_ID=your-spreadsheet-id
```

### 2. Platform-Specific Setup

#### Railway
1. Go to your Railway project dashboard
2. Navigate to Variables tab
3. Add each environment variable individually
4. Deploy your updated code

#### Heroku
```bash
heroku config:set GOOGLE_CLOUD_PROJECT_ID=your-project-id
heroku config:set GOOGLE_CLOUD_PRIVATE_KEY_ID=your-private-key-id
heroku config:set GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
heroku config:set GOOGLE_CLOUD_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
# ... continue with other variables
```

#### Docker
Update your docker-compose.yml or .env file with the new variables (already done in this migration).

### 3. Local Development

1. Create a `.env` file from `env.example`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your actual values (from your original JSON file)
3. Never commit the `.env` file to version control

## 🔒 Security Benefits

- ✅ **No credential files in codebase**: Eliminates risk of accidentally committing secrets
- ✅ **Environment-specific configuration**: Different credentials for dev/staging/production
- ✅ **Platform compatibility**: Works with all major deployment platforms
- ✅ **Audit trail**: Better tracking of credential usage
- ✅ **Rotation friendly**: Easy to update credentials without code changes

## 🚨 Important Notes

1. **Private Key Format**: The private key must include `\n` characters for line breaks
2. **Quotes**: Wrap the private key in double quotes to preserve formatting
3. **Original Values**: Use the values from your original JSON credential file
4. **Git Ignore**: JSON credential files are now ignored by Git

## 🧪 Testing the Migration

After setting up environment variables, test the application:

1. Start the application locally
2. Try the keyword search functionality
3. Check that Google Sheets integration works
4. Verify no errors in logs

## 🆘 Troubleshooting

### Error: "Missing required Google Cloud credentials"
- Check that all required environment variables are set
- Verify the variable names match exactly (case-sensitive)

### Error: "Failed to initialize Google Cloud credentials"
- Check the private key format (must include \n characters)
- Ensure the private key is wrapped in quotes
- Verify the client email format

### Connection Issues
- Verify the project ID is correct
- Check that the service account has proper permissions
- Ensure the spreadsheet ID is valid

## 📝 Where to Find Your Credentials

If you need to find your original credential values:
1. Check your Google Cloud Console
2. Look for the original JSON file (if you have a backup)
3. Download a new service account key if needed

**Important**: Never commit actual credential values to version control!