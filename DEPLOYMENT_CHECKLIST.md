# 📋 PythonAnywhere Deployment Checklist

## Pre-Deployment ✅

- [ ] GitHub account exists
- [ ] Repository cloned to local
- [ ] PythonAnywhere account created (username: **udayoption**)
- [ ] Anthropic API key ready (from https://console.anthropic.com)

---

## Terminal Commands (Copy & Paste in PythonAnywhere Bash Console)

### Step 1: Clone Repo
```bash
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
```
✅ **Check**: Should see manage.py and folders

---

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip
```
✅ **Check**: (optionchain) appears in bash prompt

---

### Step 3: Install All Packages
```bash
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
```
✅ **Check**: "Successfully installed" message

---

### Step 4: Run Database Migrations
```bash
cd ~/OptionChain-Analyser_CSV
python manage.py migrate
```
✅ **Check**: "Operations to perform: ... OK"

---

### Step 5: Create Directories
```bash
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
```
✅ **Check**: Directories created

---

### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```
✅ **Check**: "123 static files copied"

---

### Step 7: Create .env File with Your API Key
```bash
cat > ~/OptionChain-Analyser_CSV/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_KEY_HERE
DEBUG=False
SECRET_KEY=django-insecure-very-long-random-string-here
EOF
```

**Then edit it:**
```bash
nano ~/OptionChain-Analyser_CSV/.env
```

- Replace `sk-ant-YOUR_ACTUAL_KEY_HERE` with your real key
- Press `Ctrl+X`, `Y`, `Enter` to save

✅ **Check**: File saved with your actual API key

---

### Step 8: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

When prompted:
- Username: `admin`
- Email: `your@email.com`
- Password: `YourStrongPassword123@`

✅ **Check**: "Superuser created successfully"

---

## Web Configuration in PythonAnywhere Dashboard

### 1. Add Web App
- [ ] Go to **pythonanywhere.com → Web**
- [ ] Click **Add a new web app**
- [ ] Choose **Manual configuration**
- [ ] Select **Python 3.10**

---

### 2. Configure WSGI File
- [ ] In **Web** tab, find **WSGI configuration file**
- [ ] Click the file path
- [ ] Replace content with code from `pythonanywhere_wsgi.py`

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

- [ ] Click **Save**

---

### 3. Set Virtualenv
- [ ] Find **Virtualenv** section
- [ ] Click and set to: `/home/udayoption/.virtualenvs/optionchain`
- [ ] Click **Save** or confirm

---

### 4. Configure Static Files
- [ ] Click **Add static files mapping**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/udayoption/OptionChain-Analyser_CSV/staticfiles` |

- [ ] Click **Add another** if needed for media
| URL | Directory |
|-----|-----------|
| `/media/` | `/home/udayoption/OptionChain-Analyser_CSV/media` |

---

### 5. Reload Web App
- [ ] Click green **RELOAD** button
- [ ] Wait 10-15 seconds

✅ **Check**: Green button shows "last reloaded X seconds ago"

---

## Test Deployment

- [ ] Open: **https://udayoption.pythonanywhere.com**
  - Should see dashboard
  
- [ ] Open: **https://udayoption.pythonanywhere.com/admin**
  - Should see login page
  
- [ ] Login with:
  - Username: `admin`
  - Password: `YourStrongPassword123@`

---

## Upload CSV Files

1. [ ] Go to **Files** tab in PythonAnywhere
2. [ ] Navigate to: `OptionChain-Analyser_CSV/stocks/`
3. [ ] Upload CSV files to `TCS/` and `ETERNAL/` folders

Or terminal:
```bash
# Copy from local to PythonAnywhere
scp -r stocks/* udayoption@ssh.pythonanywhere.com:~/OptionChain-Analyser_CSV/stocks/
```

---

## Troubleshooting

### ❌ Error: ModuleNotFoundError

**Solution**: Check virtualenv path and WSGI configuration

```bash
workon optionchain
pip install -r requirements.txt
```

Then reload web app.

---

### ❌ Error: Static files not loading

**Solution**: Recollect static files

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py collectstatic --noinput
```

Then reload web app.

---

### ❌ Error: API key not found

**Solution**: Check .env file

```bash
cat ~/OptionChain-Analyser_CSV/.env
```

Should show your API key. If not, edit:

```bash
nano ~/OptionChain-Analyser_CSV/.env
```

---

### ❌ Error: 502 Bad Gateway

**Solution**: Check error logs

```bash
tail -f /var/log/udayoption.pythonanywhere_com_error.log
```

Fix issues and reload.

---

## Success! 🎉

Your website is now live at:

### **https://udayoption.pythonanywhere.com**

| Item | Value |
|------|-------|
| **Website** | https://udayoption.pythonanywhere.com |
| **Admin** | https://udayoption.pythonanywhere.com/admin |
| **Username** | udayoption |
| **Database** | SQLite3 (local) |
| **Storage** | 512MB free tier |

---

## What's Working

✅ Dashboard - view stocks  
✅ CSV Upload - upload option chain files  
✅ Reports - run algorithms  
✅ Admin Panel - manage data  
✅ Predictions - view AI predictions  
✅ Outcome Feed - validate predictions  

---

## Next Steps

1. Upload sample CSV files
2. Fill market context form
3. View algorithm predictions
4. Feed outcomes next day
5. Watch system learn and improve

---

**Happy Trading! 🎯📈**
