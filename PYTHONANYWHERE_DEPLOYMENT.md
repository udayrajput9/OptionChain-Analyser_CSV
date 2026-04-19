# PythonAnywhere Deployment Guide - OptionChain-Analyser

**Username**: udayoption  
**Project**: OptionChain-Analyser  
**Domain**: udayoption.pythonanywhere.com

---

## 📋 Full Deployment Terminal Commands

### STEP 1: Login to PythonAnywhere Web Console

Go to: **https://www.pythonanywhere.com**

1. Sign up with username: **udayoption**
2. Go to **Web** section
3. Add a new web app (Select Django 4.2 + Python 3.10)

---

### STEP 2: Open Bash Console

Go to: **https://www.pythonanywhere.com/consoles/**  
Click: **Start a new Bash console**

Copy and paste the commands below one by one:

---

## 🚀 TERMINAL COMMANDS (Copy & Paste)

### Command 1: Navigate to home and clone repo
```bash
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
ls -la
```

**Expected Output**: You should see `manage.py`, `requirements.txt`, folders like `dashboard`, `optionchain_project`, etc.

---

### Command 2: Create virtual environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip
```

**Expected Output**: Virtual environment created, pip upgraded

---

### Command 3: Install all requirements
```bash
pip install Django==4.2.9
pip install gunicorn==21.2.0
pip install whitenoise==6.5.0
pip install psycopg2-binary==2.9.9
pip install pandas==2.1.4
pip install numpy==1.24.3
pip install anthropic==0.7.1
pip install python-dotenv==1.0.0
```

**Or install all at once:**
```bash
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
```

---

### Command 4: Run migrations
```bash
cd ~/OptionChain-Analyser_CSV
python manage.py migrate
```

**Expected Output**: "Operations to perform: ... Applying ... OK"

---

### Command 5: Create superuser (admin)
```bash
python manage.py createsuperuser
```

**When prompted, enter:**
- Username: `admin`
- Email: `your@email.com`
- Password: `YourStrongPassword123!`
- Confirm: (repeat password)

---

### Command 6: Collect static files
```bash
python manage.py collectstatic --noinput
```

**Expected Output**: "123 static files copied to '/home/udayoption/OptionChain-Analyser_CSV/staticfiles'"

---

### Command 7: Create required directories
```bash
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
```

---

### Command 8: Create .env file with API key
```bash
cat > ~/OptionChain-Analyser_CSV/.env << 'EOF'
ANTHROPIC_API_KEY=your_actual_api_key_here
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
EOF
```

**Edit and add your actual Anthropic API key:**
```bash
nano ~/OptionChain-Analyser_CSV/.env
```

Then:
- Find: `ANTHROPIC_API_KEY=your_actual_api_key_here`
- Replace with: `ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx`
- Press `Ctrl+X`, then `Y`, then `Enter` to save

---

## ⚙️ STEP 3: Configure PythonAnywhere Web App

### Go to Web Tab in PythonAnywhere

1. Click: **Web** → **Add a new web app**
2. Choose: **Manual configuration**
3. Select: **Python 3.10**

---

### Configure WSGI File

1. In **Web** tab, find **WSGI configuration file**
2. Click the file path: `/var/www/udayoption_pythonanywhere_com_wsgi.py`
3. Replace entire content with:

```python
import os
import sys

# Add project directory to path
path = os.path.expanduser('~/OptionChain-Analyser_CSV')
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'optionchain_project.settings'

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Click: Save**

---

### Set Virtualenv Path

1. In **Web** tab, find **Virtualenv**
2. Click and set to: `/home/udayoption/.virtualenvs/optionchain`

---

### Configure Static Files

In **Web** tab, set **Static files** mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/udayoption/OptionChain-Analyser_CSV/staticfiles` |
| `/media/` | `/home/udayoption/OptionChain-Analyser_CSV/media` |

---

## 📝 STEP 4: Update Settings.py for PythonAnywhere

Open file in Bash:
```bash
nano ~/OptionChain-Analyser_CSV/optionchain_project/settings.py
```

Find the bottom of the file and add:

```python
# PythonAnywhere Configuration
import os
from pathlib import Path

if 'pythonanywhere' in os.environ.get('HOME', ''):
    ALLOWED_HOSTS = ['udayoption.pythonanywhere.com', 'www.udayoption.pythonanywhere.com', 'localhost', '127.0.0.1']
    DEBUG = False
    
    # Static files configuration
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    
    # Database - use SQLite by default (PythonAnywhere supports it)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
    # Security
    CSRF_TRUSTED_ORIGINS = ['https://udayoption.pythonanywhere.com']
    SECURE_SSL_REDIRECT = False  # Set to True if using HTTPS
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    
    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            },
        },
        'root': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    }
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

## 🔄 STEP 5: Reload Web App

Go back to **PythonAnywhere** → **Web** tab

Click the green **Reload** button

Wait 10-15 seconds for it to reload...

---

## ✅ STEP 6: Test Your Deployment

### Open in Browser:
```
https://udayoption.pythonanywhere.com
```

You should see the OptionChain-Analyser dashboard!

### Admin Panel:
```
https://udayoption.pythonanywhere.com/admin
```

Login with:
- Username: `admin`
- Password: `YourStrongPassword123!` (from Step 5)

---

## 🐛 Troubleshooting

### If you get 502/500 error:

Go to **Web** → **Error logs** and check:

```bash
tail -f /var/log/udayoption.pythonanywhere_com_error.log
```

### If static files not loading:

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py collectstatic --noinput
```

Then reload web app.

### If database error:

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py migrate
```

---

## 📤 Upload CSV Files

1. Go to **Files** tab in PythonAnywhere
2. Navigate to: `OptionChain-Analyser_CSV/stocks/`
3. Create folders: `TCS`, `ETERNAL` (if not exist)
4. Upload your CSV files there

Or use terminal:
```bash
cd ~/OptionChain-Analyser_CSV/stocks/
mkdir TCS ETERNAL
```

---

## 🔑 Setting Anthropic API Key

### Option 1: Set in .env file (Recommended)

```bash
nano ~/OptionChain-Analyser_CSV/.env
```

Add/Edit:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

### Option 2: Set as Environment Variable

In PythonAnywhere **Web** tab, find **Environment variables** and add:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

Then reload web app.

---

## 📊 Useful PythonAnywhere Commands

### View Live Logs
```bash
tail -f /var/log/udayoption.pythonanywhere_com.log
```

### Check Disk Usage
```bash
du -sh ~/OptionChain-Analyser_CSV
```

### Check Python Version
```bash
source /home/udayoption/.virtualenvs/optionchain/bin/activate
python --version
```

### Re-install all packages (if issues)
```bash
source /home/udayoption/.virtualenvs/optionchain/bin/activate
pip install --force-reinstall Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 anthropic==0.7.1 pandas==2.1.4 numpy==1.24.3
```

---

## 🌐 Final Result

Once deployed, your website will be at:

### 🎯 **https://udayoption.pythonanywhere.com**

Features available:
- ✅ Dashboard (/)
- ✅ CSV Upload (/upload/)
- ✅ Reports (/report/)
- ✅ Predictions (/prediction/)
- ✅ Outcome Feed (/outcome/)
- ✅ Admin Panel (/admin)

---

## 📞 Quick Reference

| Item | Value |
|------|-------|
| **Website URL** | https://udayoption.pythonanywhere.com |
| **Admin Panel** | https://udayoption.pythonanywhere.com/admin |
| **Admin User** | admin |
| **Virtual Environment** | /home/udayoption/.virtualenvs/optionchain |
| **Project Directory** | /home/udayoption/OptionChain-Analyser_CSV |
| **Database** | /home/udayoption/OptionChain-Analyser_CSV/db.sqlite3 |
| **Username** | udayoption |

---

**Version**: 1.0  
**Last Updated**: April 19, 2026  
**Status**: Ready to Deploy ✅
