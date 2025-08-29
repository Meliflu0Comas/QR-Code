# 🎯 QR Code Generator

A modern, web-based QR code generator with multiple styling options and real-time preview.

![QR Code Generator](https://img.shields.io/badge/Python-Flask-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Live Preview** - See QR codes as you type
- **Multiple Styles** - Square, Rounded, Circle, Gapped modules
- **Color Customization** - Choose any colors with gradient effects
- **Dual Export** - Download as PNG or SVG formats
- **Mobile Responsive** - Works on all devices
- **No Registration** - Use immediately

## 🚀 Live Demo

**Deployed on PythonAnywhere:** [Visit App](https://yourusername.pythonanywhere.com)

## 🛠️ Technologies

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **QR Generation:** qrcode library with PIL/Pillow
- **Deployment:** PythonAnywhere

## 🔧 Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/qr-generator.git
cd qr-generator

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Open browser
http://localhost:5000
```

## 📦 Dependencies

- Flask 2.3.3
- Flask-CORS 4.0.0  
- qrcode[pil] 7.4.2
- Pillow 10.0.1

## 🚀 Deployment on PythonAnywhere

### Step 1: Upload Code
```bash
# On PythonAnywhere Bash console
git clone https://github.com/Meliflu0Comas/QR-Code.git
cd QR-Code
```

### Step 2: Install Dependencies
```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 qr-generator
pip install -r requirements.txt
```

### Step 3: Configure Web App
1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** → **Python 3.10**
4. Set **Source code:** `/home/yourusername/QR-Code`
5. Set **WSGI configuration file:** `/home/yourusername/QR-Code/wsgi.py`

### Step 4: Update WSGI File
Edit the `wsgi.py` file and replace `yourusername` with your actual PythonAnywhere username.

### Step 5: Static Files (Optional)
Add static files mapping:
- **URL:** `/static/`  
- **Directory:** `/home/yourusername/QR-Code/static/`

### Step 6: Reload Web App
Click **Reload** on the Web tab and visit `https://yourusername.pythonanywhere.com`

## 🔧 Alternative: Railway Deployment

This app is also configured for Railway deployment with the included `Procfile`.

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

Made with ❤️ using Python Flask