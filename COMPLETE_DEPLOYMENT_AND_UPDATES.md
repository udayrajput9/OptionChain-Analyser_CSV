# 🎯 Complete PythonAnywhere Deployment & Update Guide
## (500MB Free Tier - Production Ready)

---

## 📖 TABLE OF CONTENTS

1. **Pre-Deployment Checklist**
2. **Initial Deployment (First Time)**
3. **How Git Works**
4. **How to Update Code**
5. **PythonAnywhere Update Commands**
6. **Troubleshooting**

---

# 🚀 SECTION 1: PRE-DEPLOYMENT CHECKLIST

Before you start, you should have:

- [ ] GitHub account with repository: https://github.com/udayrajput9/OptionChain-Analyser_CSV
- [ ] PythonAnywhere account (sign up at pythonanywhere.com)
- [ ] Anthropic API key (from https://console.anthropic.com)
- [ ] Project code ready locally

**Files You Should Have**:
- ✅ PYTHONANYWHERE_500MB_FREE_TIER.md
- ✅ GIT_AND_UPDATE_GUIDE.md
- ✅ PYTHONANYWHERE_DEPLOYMENT.md
- ✅ Updated settings.py (with free tier config)
- ✅ .gitignore file

---

# 🌐 SECTION 2: INITIAL DEPLOYMENT

### Step 1: Create PythonAnywhere Account

1. Go to: https://www.pythonanywhere.com
2. Sign up with username: **udayoption**
3. Verify email

### Step 2: Open Bash Console

1. Log in to PythonAnywhere
2. Go to: **Consoles** tab
3. Click: **"Start a new Bash console"**

### Step 3: Copy & Paste Complete Deployment Script

**In the Bash console, copy-paste this entire script:**

```bash
#!/bin/bash
# OptionChain-Analyser - Initial Setup for PythonAnywhere 500MB

echo "=== STEP 1: Clone Repository ==="
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
echo "✅ Repository cloned"

echo ""
echo "=== STEP 2: Create Virtual Environment ==="
mkvirtualenv --python=/usr/bin/python3.10 optionchain
pip install --upgrade pip setuptools wheel
echo "✅ Virtual environment created"

echo ""
echo "=== STEP 3: Install Packages ==="
pip install Django==4.2.9 gunicorn==21.2.0 whitenoise==6.5.0 psycopg2-binary==2.9.9 pandas==2.1.4 numpy==1.24.3 anthropic==0.7.1 python-dotenv==1.0.0
echo "✅ All packages installed"

echo ""
echo "=== STEP 4: Setup Database ==="
python manage.py migrate
echo "✅ Database ready"

echo ""
echo "=== STEP 5: Create Directories ==="
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
echo "✅ Directories created"

echo ""
echo "=== STEP 6: Collect Static Files ==="
python manage.py collectstatic --noinput
echo "✅ Static files collected"

echo ""
echo "=== STEP 7: Check Storage Usage ==="
du -sh ~/OptionChain-Analyser_CSV
echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "NEXT STEPS:"
echo "1) Edit .env file: nano ~/OptionChain-Analyser_CSV/.env"
echo "   - Replace: sk-ant-YOUR_KEY_HERE with your API key"
echo "   - Save: Ctrl+X → Y → Enter"
echo ""
echo "2) Create admin: python manage.py createsuperuser"
echo ""
echo "3) Go to Web tab in PythonAnywhere and:"
echo "   - Configure WSGI file"
echo "   - Set virtualenv"
echo "   - Add static files mapping"
echo "   - Click RELOAD"
```

**Your bash will run for 30-60 seconds**. Wait for ✅ completion message.

### Step 4: Setup .env File with API Key

```bash
nano ~/OptionChain-Analyser_CSV/.env
```

You'll see:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
DEBUG=False
SECRET_KEY=...
PYTHONANYWHERE=True
```

**Edit it:**
1. Find: `sk-ant-YOUR_KEY_HERE`
2. Replace with your actual key from: https://console.anthropic.com/account/keys
3. Save: Press `Ctrl+X`, then `Y`, then `Enter`

### Step 5: Create Admin User

```bash
cd ~/OptionChain-Analyser_CSV
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `your@email.com`
- Password: `YourStrongPassword123`

### Step 6: Configure Web App in PythonAnywhere

#### 6.1: Add Web App

1. Click: **Web** tab in PythonAnywhere
2. Click: **"Add a new web app"**
3. Choose: **Manual configuration**
4. Select: **Python 3.10**

#### 6.2: Setup Virtualenv

1. Find: **Virtualenv** section
2. Set to: `/home/udayoption/.virtualenvs/optionchain`
3. Save

#### 6.3: Edit WSGI File

1. Find: **WSGI configuration file**
2. Click the file path to edit
3. Replace entire content with:

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

4. Click: **Save**

#### 6.4: Add Static Files Mapping

1. Find: **Static files** section
2. Add mapping:
   - URL: `/static/`
   - Directory: `/home/udayoption/OptionChain-Analyser_CSV/staticfiles`
3. Click: **Add**

#### 6.5: Click RELOAD

1. Find: Green **RELOAD** button
2. Click it
3. Wait 10-15 seconds

✅ **Your website is now live at: https://udayoption.pythonanywhere.com**

---

# 🔄 SECTION 3: UNDERSTANDING GIT

### What is Git?

Git is version control system. Think of it as:
- **Local**: Your computer (has full history)
- **GitHub**: Cloud backup (online repository)

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

### The 3-Step Git Workflow

```bash
# STEP 1: Add files you changed
git add -A

# STEP 2: Commit (save with message)
git commit -m "Your message describing change"

# STEP 3: Push to GitHub
git push origin main
```

### Why Use Git?

✅ Track all changes  
✅ Easy to revert if something breaks  
✅ Can work with others  
✅ Backup in cloud  

---

# 💻 SECTION 4: HOW TO UPDATE CODE

### Scenario A: You Found & Fixed a Bug

**On Your Computer:**

```bash
# 1. Edit the file (e.g., dashboard/views.py)
# 2. Save file in VS Code

# 3. Check what changed
git status

# 4. Add changes
git add -A

# 5. Commit (save)
git commit -m "Fix: description of bug fix"

# 6. Push to GitHub
git push origin main
```

### Scenario B: You Want to Update PythonAnywhere Website

**On Your Computer:**
```bash
git add -A
git commit -m "Update: new feature"
git push origin main
```

**On PythonAnywhere (after push):**
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Then click RELOAD in Web tab
```

### Scenario C: You Only Changed Code (No Settings)

**Fastest method:**

On PythonAnywhere:
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# Just click RELOAD
```

No need to recollect static files.

---

# 🌐 SECTION 5: PYTHONANYWHERE UPDATE COMMANDS

### After You Push Code to GitHub

**In PythonAnywhere Bash Console, use these commands:**

#### Quick Update (Code Only)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# Click RELOAD in Web tab
```

#### Standard Update (Code + Static Files)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Click RELOAD in Web tab
```

#### Full Update (Everything)
```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Click RELOAD in Web tab
```

#### Check Storage After Update
```bash
du -sh ~/OptionChain-Analyser_CSV
```

Should show: ~300-400MB (well under 500MB limit)

---

# 🎯 COMPLETE WORKFLOW EXAMPLE

## Example: Fixing Decimal Serialization Error

### Step 1: Local Machine (Your Computer)

```bash
# 1. Edit file
# (Open dashboard/views.py in VS Code)
# (Make changes to fix bug)

# 2. Save file in VS Code (Ctrl+S)

# 3. Check git status
cd c:\Users\ASUS\Pictures\Option_Analyser\optionchain_project
git status

# Output:
# Changes not staged for commit:
#   modified: dashboard/views.py

# 4. Add the change
git add dashboard/views.py

# 5. Verify it's added
git status

# Output:
# Changes to be committed:
#   modified: dashboard/views.py

# 6. Commit (save with message)
git commit -m "Fix: Decimal serialization in report view"

# Output:
# [main abc1234] Fix: Decimal serialization in report view
#  1 file changed, 10 insertions(+), 5 deletions(-)

# 7. Push to GitHub
git push origin main

# Output:
# To https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
#    old1234..xyz5678  main -> main
```

### Step 2: PythonAnywhere

```bash
# 1. Go to PythonAnywhere → Consoles → Bash

# 2. Navigate to project
cd ~/OptionChain-Analyser_CSV

# 3. Get latest code from GitHub
git pull origin main

# Output:
# Updating old1234..xyz5678
# Fast-forward
#  dashboard/views.py | 15 +++++++++------
#  1 file changed, 10 insertions(+), 5 deletions(-)

# 4. Activate environment
workon optionchain

# 5. Recollect static files (if any were changed)
python manage.py collectstatic --noinput

# 6. Go to Web tab and click green RELOAD button in PythonAnywhere dashboard

# 7. Test your fix
# Open in browser: https://udayoption.pythonanywhere.com/report/ETERNAL/2/
# Should work now!
```

---

# 🆘 SECTION 6: TROUBLESHOOTING

### Problem: "git: not a git repository"

**Solution:**
```bash
cd ~/OptionChain-Analyser_CSV
git status
```

Make sure you're in the project directory.

### Problem: "Permission denied" when pushing

**Solution:**  
Add SSH key to GitHub:
1. Generate: `ssh-keygen -t ed25519 -C "your@email.com"`
2. Get public key: `cat ~/.ssh/id_ed25519.pub`
3. Add to GitHub: https://github.com/settings/ssh

Or use HTTPS (easier):
```bash
git remote set-url origin https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
```

### Problem: Website shows 500 error after updating

**Solution:**
```bash
# Check error log
tail -f /var/log/udayoption.pythonanywhere_com_error.log

# Recollect static files
cd ~/OptionChain-Analyser_CSV
workon optionchain
python manage.py collectstatic --noinput

# Go to Web tab and RELOAD again
```

### Problem: Storage is full (> 500MB)

**Solution:**
```bash
# Check what's taking space
du -sh ~/OptionChain-Analyser_CSV/*

# Delete old logs
rm ~/OptionChain-Analyser_CSV/logs/*

# Delete old CSVs (only if you're done with them)
# rm ~/OptionChain-Analyser_CSV/stocks/TCS/*.csv

# Check again
du -sh ~/OptionChain-Analyser_CSV
```

### Problem: Database error after migration

**Solution:**
```bash
cd ~/OptionChain-Analyser_CSV
workon optionchain
python manage.py migrate
python manage.py migrate --fake-initial  # If stuck
```

---

# 📋 QUICK REFERENCE CARD

## Git Commands

| Command | What It Does |
|---------|------------|
| `git status` | See what changed |
| `git add -A` | Add all changes |
| `git add file.py` | Add specific file |
| `git commit -m "msg"` | Save changes locally |
| `git push origin main` | Upload to GitHub |
| `git pull origin main` | Download from GitHub |
| `git log --oneline` | See commit history |

## PythonAnywhere Commands

| Command | What It Does |
|---------|------------|
| `cd ~/OptionChain-Analyser_CSV` | Go to project |
| `workon optionchain` | Activate environment |
| `git pull origin main` | Get latest code |
| `python manage.py migrate` | Run migrations |
| `python manage.py collectstatic --noinput` | Update static files |
| `du -sh .` | Check storage usage |

## PythonAnywhere Steps

1. Edit code locally
2. `git add`, `git commit`, `git push`
3. PythonAnywhere: `git pull`, run commands
4. Click RELOAD button in Web tab
5. Test at: https://udayoption.pythonanywhere.com

---

# ✅ YOUR COMPLETE SETUP

## Files in GitHub

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
- ✅ settings.py - (Updated with free tier config)

## Website

- **URL**: https://udayoption.pythonanywhere.com
- **Admin**: https://udayoption.pythonanywhere.com/admin
- **Storage**: 500MB free tier
- **Always Running**: 24/7

## Status

✅ **Everything is ready to deploy!**

---

# 🎉 YOU'RE ALL SET!

**Next step**: Follow PYTHONANYWHERE_500MB_FREE_TIER.md or PYTHONANYWHERE_DEPLOYMENT.md for deployment.

After deployment, use this guide for updates.

---

**Questions?** Check:
1. GIT_AND_UPDATE_GUIDE.md
2. PYTHONANYWHERE_500MB_FREE_TIER.md
3. TROUBLESHOOTING section above

**Happy Trading! 🎯📈**
