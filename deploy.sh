#!/bin/bash
# Deployment script for QR Code Generator

echo "🚀 Preparing QR Code Generator for deployment..."

# Create deployment directory
mkdir -p deploy

# Copy necessary files
cp app.py deploy/
cp requirements.txt deploy/
cp -r templates deploy/

# Create production requirements (if needed)
echo "Flask==2.3.3" > deploy/requirements_prod.txt
echo "Flask-CORS==4.0.0" >> deploy/requirements_prod.txt
echo "qrcode[pil]==7.4.2" >> deploy/requirements_prod.txt
echo "Pillow==10.0.1" >> deploy/requirements_prod.txt

echo "✅ Deployment files ready in 'deploy' folder"
echo ""
echo "📋 Next steps for HostGator:"
echo "1. Upload contents of 'deploy' folder to your hosting"
echo "2. Set up Python app in cPanel (if supported)"
echo "3. Install requirements: pip install -r requirements.txt"
echo "4. Point domain to app.py"
echo ""
echo "🌐 Alternative: Use Heroku, PythonAnywhere, or Railway for easier Python hosting"
