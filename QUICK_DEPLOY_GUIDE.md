# 🚀 PythonAnywhere Deployment - Step-by-Step Guide

**Username**: udayoption  
**Website**: https://udayoption.pythonanywhere.com  
**Repository**: https://github.com/udayrajput9/OptionChain-Analyser_CSV

---

## 📊 What You Have Ready

Your repository now has complete deployment files:

```
├── PYTHONANYWHERE_DEPLOYMENT.md      ⭐ Full deployment guide
├── DEPLOYMENT_CHECKLIST.md           ✅ Step-by-step checklist
├── deploy_pythonanywhere.sh          🔧 Deployment script
├── pythonanywhere_wsgi.py            ⚙️ WSGI configuration
├── .env.example                      🔑 Environment template
├── Procfile                          📦 Process file
└── README.md                         📖 Project documentation
```

---

## 🎯 Quick Start (5 Steps)

### Step 1: Create PythonAnywhere Account

1. Go to: **https://www.pythonanywhere.com**
2. Sign up with username: **udayoption**
3. Create account (free tier available)

---

### Step 2: Open Bash Console

1. Log in to PythonAnywhere
2. Go to: **Consoles** tab
3. Click: **Start a new Bash console**

---

### Step 3: Copy & Paste Terminal Commands

Paste these commands one by one (or use the script):

**Option A: Copy Entire Script**
```bash
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
python manage.py migrate
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
python manage.py collectstatic --noinput
```

**Option B: Step-by-Step** (See PYTHONANYWHERE_DEPLOYMENT.md)

---

### Step 4: Setup .env File with API Key

In bash:
```bash
nano ~/OptionChain-Analyser_CSV/.env
```

Add:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_KEY_HERE
DEBUG=False
SECRET_KEY=django-insecure-make-this-very-long-and-random
```

Save: `Ctrl+X` → `Y` → `Enter`

Replace `sk-ant-YOUR_ACTUAL_KEY_HERE` with your real key from:
https://console.anthropic.com/account/keys

---

### Step 5: Configure Web App

1. Click: **Web** tab in PythonAnywhere
2. Click: **Add a new web app**
3. Choose: **Manual configuration** → **Python 3.10**
4. Set **Virtualenv** to: `/home/udayoption/.virtualenvs/optionchain`
5. Edit **WSGI configuration file**:

```python
import os
import sys

path = os.path.expanduser('~/OptionChain-Analyser_CSV')
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'optionchain_project.settings'

from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Add **Static files**:
   - URL: `/static/`
   - Directory: `/home/udayoption/OptionChain-Analyser_CSV/staticfiles`

7. Click **RELOAD** button (green)
8. Wait 10-15 seconds

---

## ✅ Done! Your Site is Live

Visit: **https://udayoption.pythonanywhere.com**

---

## 🔑 Create Admin User

After deployment, in bash:
```bash
cd ~/OptionChain-Analyser_CSV
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `your@email.com`
- Password: `YourStrongPassword123@`

Then login at: **https://udayoption.pythonanywhere.com/admin**

---

## 📁 Access Your Files

1. Go to **Files** tab in PythonAnywhere
2. Upload CSV files to: `/home/udayoption/OptionChain-Analyser_CSV/stocks/`
3. Create folders: `TCS/`, `ETERNAL/`, etc.
4. Upload your `.csv` files there

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| [PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md) | 📚 Complete deployment guide with all commands |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | ✅ Checkbox checklist to follow |
| [README.md](README.md) | 📖 Project documentation |
| [.env.example](.env.example) | 🔑 Environment variables template |
| [pythonanywhere_wsgi.py](pythonanywhere_wsgi.py) | ⚙️ WSGI configuration |

---

## 🎯 Website URLs

After deployment:

| URL | Purpose |
|-----|---------|
| https://udayoption.pythonanywhere.com | 🏠 Dashboard |
| https://udayoption.pythonanywhere.com/admin | 🔐 Admin panel |
| https://udayoption.pythonanywhere.com/upload/ | 📤 CSV upload |
| https://udayoption.pythonanywhere.com/report/ | 📊 Reports |
| https://udayoption.pythonanywhere.com/prediction/ | 🤖 AI predictions |
| https://udayoption.pythonanywhere.com/outcome/ | ✅ Outcome feed |

---

## 🐛 If Something Goes Wrong

### Error: ModuleNotFoundError

```bash
cd ~/OptionChain-Analyser_CSV
workon optionchain
pip install -r requirements.txt
```

Then reload web app.

### Error: Static files not working

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py collectstatic --noinput
```

Then reload.

### Error: 500/502 Error

Check error logs in PythonAnywhere:
- **Web** tab → **Error logs**
- Or in bash:
```bash
tail -f /var/log/udayoption.pythonanywhere_com_error.log
```

---

## 📞 Important Notes

### API Key Required
Your site needs Anthropic API key for Claude AI features. Get it free from: https://console.anthropic.com

**Free Tier**: 
- $5 free credits monthly (enough for personal use)
- Pay-as-you-go after credits exhaust

### PythonAnywhere Limits
- Free tier: 512MB storage
- Free tier: Limited CPU
- No file uploads > 100MB
- Good enough for testing & demo

### Always Running
✅ Yes - website runs 24/7 on free tier

---

## 💡 Tips

1. **Keep API Key Safe** - Don't commit .env to GitHub
2. **Upload Sample CSVs** - Put test files in stocks/TCS/ and stocks/ETERNAL/
3. **Check Logs Often** - If errors, check PythonAnywhere error logs
4. **Reload After Changes** - Click RELOAD button after any code changes
5. **Scale Later** - Upgrade plan if you need more power later

---

## 📊 Your Deployment Stack

| Component | Details |
|-----------|---------|
| **Hosting** | PythonAnywhere (free tier) |
| **Language** | Python 3.10 |
| **Framework** | Django 4.2.9 |
| **Database** | SQLite3 |
| **AI** | Claude 3 Opus (Anthropic) |
| **Storage** | 512MB (free tier) |
| **Domain** | udayoption.pythonanywhere.com |

---

## 🎉 Success Indicators

✅ Website loads at udayoption.pythonanywhere.com  
✅ Can upload CSV files  
✅ Can see algorithm predictions  
✅ Admin panel accessible at /admin  
✅ Static files loading (CSS, JS visible)  

---

## 🚀 Next: Production Optimization (Optional)

After deployment works, you can:
- Upgrade to paid PythonAnywhere plan ($5/month)
- Add custom domain
- Increase storage to 2GB
- Better CPU performance

---

## 📚 Learning Resources

- PythonAnywhere Docs: https://help.pythonanywhere.com
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Anthropic Claude: https://docs.anthropic.com

---

**Status**: ✅ Ready to Deploy  
**Last Updated**: April 19, 2026  
**Repository**: https://github.com/udayrajput9/OptionChain-Analyser_CSV

---

**Happy Trading! 🎯📈**

Questions? Check:
1. PYTHONANYWHERE_DEPLOYMENT.md - Complete guide
2. DEPLOYMENT_CHECKLIST.md - Follow steps
3. PythonAnywhere Help: https://help.pythonanywhere.com
