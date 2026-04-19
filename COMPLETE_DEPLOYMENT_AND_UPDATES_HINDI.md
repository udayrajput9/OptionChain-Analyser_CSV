# 🎯 Complete PythonAnywhere Deployment & Update Guide
## हिंदी संस्करण (500MB Free Tier - Production Ready)

---

## 📖 विषय सूची

1. **Deployment से पहले की चेकलिस्ट**
2. **पहली बार Deployment करना**
3. **Git कैसे काम करता है?**
4. **Code कैसे Update करें**
5. **PythonAnywhere Update Commands**
6. **समस्या का समाधान**

---

# 🚀 सेक्शन 1: DEPLOYMENT FROM BEFORE CHECKLIST

शुरु करने से पहले आपके पास होना चाहिए:

- [ ] GitHub account: https://github.com/udayrajput9/OptionChain-Analyser_CSV
- [ ] PythonAnywhere account (pythonanywhere.com पर sign up करें)
- [ ] Anthropic API key (https://console.anthropic.com से)
- [ ] Project code तैयार हो

**आपके पास ये फाइलें होनी चाहिए**:
- ✅ PYTHONANYWHERE_500MB_FREE_TIER.md
- ✅ GIT_AND_UPDATE_GUIDE.md
- ✅ PYTHONANYWHERE_DEPLOYMENT.md
- ✅ Updated settings.py (free tier config के साथ)
- ✅ .gitignore file

---

# 🌐 सेक्शन 2: INITIAL DEPLOYMENT करने के Steps

### Step 1: PythonAnywhere Account बनाएं

1. जाएं: https://www.pythonanywhere.com
2. Username लिखें: **udayoption**
3. Email verify करें

### Step 2: Bash Console खोलें

1. PythonAnywhere में login करें
2. **Consoles** tab पर जाएं
3. **"Start a new Bash console"** पर क्लिक करें

### Step 3: पूरा Script Copy-Paste करें

**Bash console में ये पूरा script copy करके paste करें:**

```bash
#!/bin/bash
# OptionChain-Analyser - PythonAnywhere 500MB के लिए Initial Setup

echo "=== STEP 1: Repository Clone करना ==="
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
echo "✅ Repository clone हो गया"

echo ""
echo "=== STEP 2: Virtual Environment बनाना ==="
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip setuptools wheel
echo "✅ Virtual environment बन गया"

echo ""
echo "=== STEP 3: सभी Packages install करना ==="
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
echo "✅ सभी packages install हो गए"

echo ""
echo "=== STEP 4: Database Setup करना ==="
python manage.py migrate
echo "✅ Database ready है"

echo ""
echo "=== STEP 5: Directories बनाना ==="
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
echo "✅ Directories बन गई हैं"

echo ""
echo "=== STEP 6: Static Files Collect करना ==="
python manage.py collectstatic --noinput
echo "✅ Static files collect हो गई हैं"

echo ""
echo "=== STEP 7: Storage Check करना ==="
du -sh ~/OptionChain-Analyser_CSV
echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "NEXT STEPS:"
echo "1) .env file को edit करें: nano ~/OptionChain-Analyser_CSV/.env"
echo "   - Replace करें: sk-ant-YOUR_KEY_HERE को अपनी API key से"
echo "   - Save करें: Ctrl+X → Y → Enter"
echo ""
echo "2) Admin बनाएं: python manage.py createsuperuser"
echo ""
echo "3) PythonAnywhere में Web tab में जाकर:"
echo "   - WSGI file configure करें"
echo "   - virtualenv set करें"
echo "   - static files mapping add करें"
echo "   - RELOAD पर क्लिक करें"
```

**Your bash 30-60 सेकंड में चलेगा**। ✅ completion message का इंतज़ार करें।

### Step 4: .env File में API Key डालें

```bash
nano ~/OptionChain-Analyser_CSV/.env
```

आपको दिखेगा:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
DEBUG=False
SECRET_KEY=...
PYTHONANYWHERE=True
```

**इसे Edit करें:**
1. ढूंढें: `sk-ant-YOUR_KEY_HERE`
2. अपनी actual key से replace करें: https://console.anthropic.com/account/keys
3. Save करें: `Ctrl+X`, फिर `Y`, फिर `Enter`

### Step 5: Admin User बनाएं

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py createsuperuser
```

ये दिखाएं:
- Username: `admin`
- Email: `your@email.com`
- Password: `YourStrongPassword123`

### Step 6: PythonAnywhere में Web App Configure करें

#### 6.1: Web App Add करें

1. **Web** tab पर क्लिक करें
2. **"Add a new web app"** पर क्लिक करें
3. **Manual configuration** चुनें
4. **Python 3.10** select करें

#### 6.2: Virtualenv Setup करें

1. **Virtualenv** section खोजें
2. Set करें: `/home/udayoption/.virtualenvs/optionchain`
3. Save करें

#### 6.3: WSGI File को Edit करें

1. **WSGI configuration file** खोजें
2. File path पर क्लिक करके edit करें
3. पूरा content replace करें:

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

4. **Save** पर क्लिक करें

#### 6.4: Static Files Mapping Add करें

1. **Static files** section खोजें
2. Mapping add करें:
   - URL: `/static/`
   - Directory: `/home/udayoption/OptionChain-Analyser_CSV/staticfiles`
3. **Add** पर क्लिक करें

#### 6.5: RELOAD पर क्लिक करें

1. Green **RELOAD** button खोजें
2. उस पर क्लिक करें
3. 10-15 सेकंड का इंतज़ार करें

✅ **आपकी website अब live है: https://udayoption.pythonanywhere.com**

---

# 🔄 सेक्शन 3: GIT को समझें

### Git क्या होता है?

Git एक version control system है। इसे समझें:
- **Local**: आपका कंप्यूटर (पूरा history है)
- **GitHub**: Cloud backup (online storage)

```
Your Computer (Local)
        ↓
    git add
        ↓
    git commit
        ↓
    git push
        ↓
    GitHub (Cloud)
```

### 3-Step Git Workflow

```bash
# STEP 1: अपना modify किया हुआ file add करें
git add -A

# STEP 2: Commit करें (save करें)
git commit -m "आपका message"

# STEP 3: GitHub को push करें
git push origin main
```

### Git क्यों use करें?

✅ सभी changes track करें  
✅ आसानी से पुरानी version पर जाएं  
✅ दूसरों के साथ काम करें  
✅ Cloud में backup रहे  

---

# 💻 सेक्शन 4: CODE कैसे UPDATE करें

### Scenario A: Bug fix की

**अपने Computer पर:**

```bash
# 1. File को edit करें (example: dashboard/views.py)
# 2. VS Code में save करें

# 3. क्या बदला, check करें
git status

# 4. Changes add करें
git add -A

# 5. Commit करें (save करें)
git commit -m "Fix: bug का description"

# 6. GitHub को push करें
git push origin main
```

### Scenario B: PythonAnywhere website update करना है

**अपने Computer पर:**
```bash
git add -A
git commit -m "Update: नई चीज़"
git push origin main
```

**PythonAnywhere पर (push के बाद):**
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# फिर Web tab में RELOAD पर क्लिक करें
```

### Scenario C: सिर्फ code बदला, settings नहीं

**सबसे तेज़ तरीका:**

PythonAnywhere पर:
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# बस Web tab में RELOAD करें
```

Static files को फिर से collect करने की ज़रूरत नहीं।

---

# 🌐 सेक्शन 5: PYTHONANYWHERE UPDATE COMMANDS

### अगर आपने GitHub को Code push किया

**PythonAnywhere Bash Console में ये commands use करें:**

#### तेज़ Update (सिर्फ Code)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# Web tab में RELOAD करें
```

#### Normal Update (Code + Static Files)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Web tab में RELOAD करें
```

#### पूरा Update (सब कुछ)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Web tab में RELOAD करें
```

#### Update के बाद Storage Check करें

```bash
du -sh ~/OptionChain-Analyser_CSV
```

दिखना चाहिए: ~300-400MB (500MB limit से कम)

---

# 🎯 COMPLETE WORKFLOW EXAMPLE

## Example: Decimal Serialization Error को ठीक करना

### Step 1: अपने Computer पर

```bash
# 1. File को edit करें
# (VS Code में dashboard/views.py खोलें)
# (Bug fix करें)

# 2. File को save करें (Ctrl+S)

# 3. Check करें क्या बदला
cd c:\Users\ASUS\Pictures\Option_Analyser\optionchain_project
git status

# Output:
# Changes not staged for commit:
#   modified: dashboard/views.py

# 4. Change को add करें
git add dashboard/views.py

# 5. Verify करें
git status

# Output:
# Changes to be committed:
#   modified: dashboard/views.py

# 6. Commit करें (message के साथ)
git commit -m "Fix: Decimal serialization in report view"

# Output:
# [main abc1234] Fix: Decimal serialization in report view
#  1 file changed, 10 insertions(+), 5 deletions(-)

# 7. GitHub को push करें
git push origin main

# Output:
# To https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
#    old1234..xyz5678  main -> main
```

### Step 2: PythonAnywhere पर

```bash
# 1. PythonAnywhere → Consoles → Bash में जाएं

# 2. Project folder में जाएं
cd ~/OptionChain-Analyser_CSV

# 3. GitHub से latest code लें
git pull origin main

# Output:
# Updating old1234..xyz5678
# Fast-forward
#  dashboard/views.py | 15 +++++++++------
#  1 file changed, 10 insertions(+), 5 deletions(-)

# 4. Environment को activate करें
workon optionchain

# 5. Static files को recollect करें
python manage.py collectstatic --noinput

# 6. PythonAnywhere dashboard में Web tab में green RELOAD बटन पर क्लिक करें

# 7. अपना fix test करें
# Browser में खोलें: https://udayoption.pythonanywhere.com/report/ETERNAL/2/
# अब काम करना चाहिए!
```

---

# 🆘 सेक्शन 6: समस्या का समाधान

### Problem: "git: not a git repository"

**समाधान:**
```bash
cd ~/OptionChain-Analyser_CSV
git status
```

यकीनी बनाएं कि आप project folder में हैं।

### Problem: "Permission denied" जब push कर रहे हो

**समाधान:**  
GitHub में SSH key add करें:
1. Generate करें: `ssh-keygen -t ed25519 -C "your@email.com"`
2. Public key लें: `cat ~/.ssh/id_ed25519.pub`
3. GitHub में add करें: https://github.com/settings/ssh

या HTTPS use करें (आसान):
```bash
git remote set-url origin https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
```

### Problem: Code update के बाद website 500 error दिखाता है

**समाधान:**
```bash
# Error log check करें
tail -f /var/log/udayoption.pythonanywhere_com_error.log

# Static files को फिर से collect करें
cd ~/OptionChain-Analyser_CSV
workon optionchain
python manage.py collectstatic --noinput

# Web tab में फिर से RELOAD करें
```

### Problem: Storage full है (> 500MB)

**समाधान:**
```bash
# Check करें कि कहाँ space ले रहा है
du -sh ~/OptionChain-Analyser_CSV/*

# पुरानी logs delete करें
rm ~/OptionChain-Analyser_CSV/logs/*

# Check करें फिर से
du -sh ~/OptionChain-Analyser_CSV
```

### Problem: Database error migration के बाद

**समाधान:**
```bash
cd ~/OptionChain-Analyser_CSV
workon optionchain
python manage.py migrate
python manage.py migrate --fake-initial  # अगर stuck हो
```

---

# 📋 QUICK REFERENCE CARD

## Git Commands

| Command | इसका मतलब |
|---------|------------|
| `git status` | क्या बदला है |
| `git add -A` | सभी changes add करें |
| `git add file.py` | एक specific file add करें |
| `git commit -m "msg"` | Locally save करें |
| `git push origin main` | GitHub को upload करें |
| `git pull origin main` | GitHub से download करें |
| `git log --oneline` | सभी commits इतिहास |

## PythonAnywhere Commands

| Command | इसका मतलब |
|---------|------------|
| `cd ~/OptionChain-Analyser_CSV` | Project folder में जाएं |
| `workon optionchain` | Environment activate करें |
| `git pull origin main` | Latest code लें |
| `python manage.py migrate` | Database migrations run करें |
| `python manage.py collectstatic --noinput` | Static files update करें |
| `du -sh .` | Storage usage check करें |

## PythonAnywhere Steps

1. Locally code को edit करें
2. `git add`, `git commit`, `git push` करें
3. PythonAnywhere में: `git pull`, commands run करें
4. Web tab में RELOAD button पर क्लिक करें
5. Test करें: https://udayoption.pythonanywhere.com

---

# ✅ आपका COMPLETE SETUP

## GitHub में Files

- ✅ README.md - Project documentation
- ✅ PYTHONANYWHERE_DEPLOYMENT.md - Detailed guide
- ✅ PYTHONANYWHERE_500MB_FREE_TIER.md - Free tier setup
- ✅ GIT_AND_UPDATE_GUIDE.md - Git & updates
- ✅ QUICK_DEPLOY_GUIDE.md - Quick start
- ✅ DEPLOYMENT_CHECKLIST.md - Checklist
- ✅ DEPLOYMENT_SUMMARY.md - Summary
- ✅ pythonanywhere_wsgi.py - WSGI config
- ✅ .env.example - Environment template
- ✅ .gitignore - Git ignore file
- ✅ settings.py - (Free tier config के साथ)

## Website

- **URL**: https://udayoption.pythonanywhere.com
- **Admin**: https://udayoption.pythonanywhere.com/admin
- **Storage**: 500MB free tier
- **हमेशा चले**: 24/7

## Status

✅ **सब कुछ deployment के लिए तैयार है!**

---

# 🎉 आप तैयार हैं!

**अगला step**: PYTHONANYWHERE_500MB_FREE_TIER.md या PYTHONANYWHERE_DEPLOYMENT.md को follow करें।

Deployment के बाद, updates के लिए इस guide को use करें।

---

**सवाल है?** Check करें:
1. GIT_AND_UPDATE_GUIDE.md
2. PYTHONANYWHERE_500MB_FREE_TIER.md
3. ऊपर TROUBLESHOOTING section

**Happy Trading! 🎯📈**
