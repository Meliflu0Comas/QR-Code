# QR Code Generator - Production Deployment

## For HostGator Shared Hosting

### Files to Upload:
- app.py (main Flask application)
- requirements.txt (Python dependencies)
- templates/index.html (web interface)

### HostGator Setup Steps:

1. **Enable Python App in cPanel:**
   - Go to cPanel > "Python App" or "Setup Python App"
   - Create new Python application
   - Choose Python 3.x (latest available)
   - Set application URL (e.g., /qr-generator)

2. **Upload Files:**
   - Upload all files to the application directory
   - Usually located in: ~/public_html/qr-generator/

3. **Install Dependencies:**
   - In cPanel Python App interface, go to "Packages"
   - Install: Flask, qrcode, Pillow, Flask-CORS
   - Or use pip install from terminal if available

4. **Configuration:**
   - Set startup file to: app.py
   - Application callable object: app

### Alternative: Manual Upload to Regular Hosting

If HostGator doesn't support Python apps:

1. **Use a Python hosting service like:**
   - Heroku (free tier available)
   - PythonAnywhere
   - Railway
   - Render

2. **Or convert to PHP version** (requires rewriting backend)

### Environment Variables (if needed):
- FLASK_ENV=production
- FLASK_DEBUG=False

### Domain Setup:
- Point your domain/subdomain to the application directory
- Update any hardcoded URLs in the code

### Security Notes:
- The app is configured with CORS for public access
- No sensitive data is stored
- All processing is stateless
