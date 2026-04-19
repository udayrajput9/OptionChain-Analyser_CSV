# 🎯 PythonAnywhere Free Tier (500MB) - Deployment & Updates Guide

**Username**: udayoption  
**Free Tier Limit**: 500MB storage  
**Website**: https://udayoption.pythonanywhere.com  

---

## ⚙️ CODE CHANGES FOR 500MB FREE TIER

### Change 1: Update `settings.py` for Free Tier

Add this at the **end** of `optionchain_project/settings.py`:

```python
# ============================================================
# PythonAnywhere Free Tier Optimization (500MB)
# ============================================================

if 'pythonanywhere' in os.environ.get('HOME', ''):
    # Compression for smaller storage
    import os
    from pathlib import Path
    
    ALLOWED_HOSTS = ['udayoption.pythonanywhere.com', 'localhost', '127.0.0.1']
    DEBUG = False
    
    # Database - Keep SQLite (no extra space needed)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Static files - Compressed
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files - Minimal
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'
    
    # Logging - Minimal (errors only)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'error.log',
            },
        },
        'loggers': {
            'django': {'handlers': ['file'], 'level': 'ERROR'},
        },
    }
    
    # Session - Database-backed (saves disk space)
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    
    # Cache - In-memory (no disk needed)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    
    # Security
    CSRF_TRUSTED_ORIGINS = ['https://udayoption.pythonanywhere.com']
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    
    # Disable unused middleware
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
```

### Change 2: Create `.gitignore` (Don't commit large files)

```
# Python
*.pyc
__pycache__/
*.egg-info/
dist/
build/

# Django
*.log
db.sqlite3
staticfiles/
media/

# Environment
.env
.venv
venv/

# CSV Files (don't commit - only reference)
stocks/*.csv
stocks/*/*.csv

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
logs/
```

### Change 3: Optimize `requirements.txt` (Remove unused packages)

```txt
Django==4.2.9
gunicorn==21.2.0
whitenoise==6.5.0
psycopg2-binary==2.9.9
pandas==2.1.4
numpy==1.24.3
anthropic==0.7.1
python-dotenv==1.0.0
```

**Storage Impact**:
- Django + dependencies: ~50MB
- Pandas + NumPy: ~200MB
- Others: ~30MB
- **Total**: ~280MB (leaves 220MB for data)

---

## 🔄 GIT WORKFLOW - How to Update Code

### Scenario 1: You Make Changes Locally & Want to Push

```bash
# In your local project directory:

# 1️⃣ Check what changed
git status

# 2️⃣ Add all changes
git add -A

# 3️⃣ Commit with message
git commit -m "Fix: description of changes"

# 4️⃣ Push to GitHub
git push origin main
```

**Example**:
```bash
git add -A
git commit -m "Optimize settings for 500MB free tier"
git push origin main
```

### Scenario 2: You Only Changed Certain Files

```bash
# Add specific files only
git add dashboard/views.py optionchain_project/settings.py

# Commit
git commit -m "Update views and settings"

# Push
git push origin main
```

### Scenario 3: Undo Last Commit (If you made mistake)

```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Or undo completely
git reset --hard HEAD~1
git push origin main --force
```

---

## 📱 PYTHONANYWHERE - How to Update After Git Push

### Method 1: Auto-Update from GitHub (Recommended)

```bash
# SSH into PythonAnywhere or use Bash Console
cd ~/OptionChain-Analyser_CSV

# 1️⃣ Pull latest changes from GitHub
git pull origin main

# 2️⃣ Collect static files again
workon optionchain
python manage.py collectstatic --noinput

# 3️⃣ Run migrations (if any)
python manage.py migrate

# 4️⃣ Reload web app
# Go to Web tab in PythonAnywhere and click RELOAD
```

### Method 2: Step-by-Step Terminal Commands for PythonAnywhere

**Copy and paste this in PythonAnywhere Bash Console:**

```bash
#!/bin/bash
# Update script for PythonAnywhere

cd ~/OptionChain-Analyser_CSV

echo "=== Pulling Latest Code ==="
git pull origin main

echo "=== Activating Virtual Environment ==="
workon optionchain

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Running Migrations ==="
python manage.py migrate

echo "=== Checking Disk Usage ==="
du -sh .

echo "✅ Update Complete!"
echo "Now: Go to Web tab and click RELOAD button"
```

---

## 📊 COMPLETE TERMINAL COMMANDS FOR PYTHONANYWHERE

### FIRST TIME DEPLOYMENT

**Copy this entire section and paste in PythonAnywhere Bash Console:**

```bash
#!/bin/bash
# OptionChain-Analyser - Initial Deployment

echo "=== Step 1: Clone Repository ==="
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
echo "✅ Repository cloned"

echo ""
echo "=== Step 2: Create Virtual Environment ==="
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip setuptools wheel
echo "✅ Virtual environment created"

echo ""
echo "=== Step 3: Install Dependencies ==="
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
echo "✅ All packages installed"

echo ""
echo "=== Step 4: Setup Database ==="
python manage.py migrate
echo "✅ Database ready"

echo ""
echo "=== Step 5: Create Directories ==="
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
echo "✅ Directories created"

echo ""
echo "=== Step 6: Collect Static Files ==="
python manage.py collectstatic --noinput
echo "✅ Static files collected"

echo ""
echo "=== Step 7: Check Storage Usage ==="
du -sh ~/OptionChain-Analyser_CSV
echo ""
echo "=== Step 8: Create .env File ==="
cat > ~/OptionChain-Analyser_CSV/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
DEBUG=False
SECRET_KEY=django-insecure-your-secret-key-here
PYTHONANYWHERE=True
EOF

echo ""
echo "✅ DEPLOYMENT SETUP COMPLETE!"
echo ""
echo "NEXT:"
echo "1️⃣ Edit .env file: nano ~/OptionChain-Analyser_CSV/.env"
echo "   - Replace: sk-ant-YOUR_KEY_HERE with your actual API key"
echo "   - Save: Ctrl+X → Y → Enter"
echo ""
echo "2️⃣ Create admin user: python manage.py createsuperuser"
echo ""
echo "3️⃣ Go to PythonAnywhere Web Dashboard and:"
echo "   - Set Virtualenv to: /home/udayoption/.virtualenvs/optionchain"
echo "   - Edit WSGI file"
echo "   - Add static files mapping"
echo "   - Click RELOAD"
echo ""
echo "4️⃣ Visit: https://udayoption.pythonanywhere.com"
```

---

### UPDATE AFTER CHANGES

**When you want to update PythonAnywhere after making code changes:**

```bash
#!/bin/bash
# Update script - Run this after git push

cd ~/OptionChain-Analyser_CSV

echo "=== Pulling Latest Code ==="
git pull origin main

echo "=== Collecting Static Files ==="
workon optionchain
python manage.py collectstatic --noinput

echo "=== Running Migrations ==="
python manage.py migrate

echo ""
echo "✅ Update Complete!"
echo "Go to Web tab and click RELOAD button"
```

---

### QUICK UPDATE (Fast Version)

If you just changed Python files (not static files):

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py migrate
# Then RELOAD in Web tab
```

---

## 🔑 IMPORTANT: Setting Your API Key

**In PythonAnywhere Bash Console:**

```bash
# Edit .env file
nano ~/OptionChain-Analyser_CSV/.env
```

You'll see:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
DEBUG=False
SECRET_KEY=django-insecure-your-secret-key-here
PYTHONANYWHERE=True
```

**Replace** `sk-ant-YOUR_KEY_HERE` with your actual key from:  
https://console.anthropic.com/account/keys

Get key at: sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

**Save**: 
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

---

## 📋 COMPLETE WORKFLOW EXAMPLE

### Example: You fixed a bug and want to deploy

**Step 1: Local Machine**
```bash
# You fixed bug in dashboard/views.py
git add dashboard/views.py
git commit -m "Fix: Decimal serialization in reports"
git push origin main
```

**Step 2: PythonAnywhere (Bash Console)**
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Then go to Web tab and click RELOAD
```

**Step 3: Test Website**
```
https://udayoption.pythonanywhere.com
```

Done! ✅

---

## 🚨 STORAGE MANAGEMENT (500MB)

### Check Current Usage
```bash
cd ~/OptionChain-Analyser_CSV
du -sh .
du -sh stocks/
du -sh staticfiles/
du -sh db.sqlite3
```

### If Storage Full (Delete old logs)
```bash
rm -rf logs/*.log
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +
```

### Don't Upload Large CSV Files
- Keep CSVs small (~1-5MB each)
- Delete old CSVs after processing
- Use File → Upload in PythonAnywhere, not git

---

## 🔄 SETTINGS.PY CHANGES - Full Code to Add

Open: `optionchain_project/settings.py`

Add this at the **very end** of file:

```python
# =============================================================
# PythonAnywhere Production Configuration (500MB Free Tier)
# =============================================================

if 'pythonanywhere' in os.environ.get('HOME', ''):
    import logging
    from pathlib import Path
    
    # Allowed hosts
    ALLOWED_HOSTS = ['udayoption.pythonanywhere.com', 'www.udayoption.pythonanywhere.com', 'localhost', '127.0.0.1']
    
    # Production mode
    DEBUG = False
    
    # Database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Static files (compressed for 500MB)
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'
    
    # Security settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {}
    CSRF_TRUSTED_ORIGINS = ['https://udayoption.pythonanywhere.com']
    
    # Session settings (use database)
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = False
    
    # Caching (in-memory, no disk)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'optionchain-cache',
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }
    
    # Logging (minimal - errors only)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'django.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
    
    # Template settings
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'dashboard' / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
```

---

## ✅ CHECKLIST FOR 500MB FREE TIER

- [ ] Added code to end of settings.py
- [ ] Created .gitignore file
- [ ] Optimized requirements.txt
- [ ] Initial deployment done
- [ ] API key added in .env
- [ ] Website loading at https://udayoption.pythonanywhere.com
- [ ] Admin accessible
- [ ] Static files loading (CSS, JS visible)
- [ ] CSV upload working
- [ ] Reports working
- [ ] Storage checked: `du -sh .` shows < 400MB

---

## 📱 REFERENCE COMMANDS

| Task | Command |
|------|---------|
| **Activate env** | `workon optionchain` |
| **Update code** | `git pull origin main` |
| **Collect statics** | `python manage.py collectstatic --noinput` |
| **Run migrations** | `python manage.py migrate` |
| **Check storage** | `du -sh .` |
| **Edit .env** | `nano .env` |
| **View logs** | `tail -f logs/*` |
| **Delete logs** | `rm logs/*` |
| **Database backup** | `cp db.sqlite3 db.backup.sqlite3` |

---

## 🎯 FINAL QUICK REFERENCE

**First Time**:
```bash
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
python manage.py migrate
python manage.py collectstatic --noinput
nano .env  # Add API key
# Then configure web app & RELOAD
```

**Updates**:
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py migrate
python manage.py collectstatic --noinput
# RELOAD in Web tab
```

---

**Version**: 1.0 - Free Tier Edition  
**Date**: April 19, 2026  
**Storage**: 500MB Optimized  
**Status**: ✅ Ready for Production
