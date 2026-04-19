# 🔄 Git & PythonAnywhere Update Guide

**How to make code changes, push to GitHub, and update PythonAnywhere**

---

## 📝 SCENARIO 1: You Want to Update Code

### Step 1: Make Changes Locally

Edit files in VS Code:
- Example: `dashboard/views.py`, `optionchain_project/settings.py`, etc.

### Step 2: Check What Changed

```bash
git status
```

You'll see list of changed files in red:
```
Changes not staged for commit:
  modified:   dashboard/views.py
  modified:   optionchain_project/settings.py
```

### Step 3: Add Changes to Git

**Option A: Add all changes**
```bash
git add -A
```

**Option B: Add specific files**
```bash
git add dashboard/views.py
git add optionchain_project/settings.py
```

### Step 4: Commit (Save) Changes

```bash
git commit -m "Fix: description of what you changed"
```

**Good commit message examples:**
```bash
git commit -m "Fix: Decimal serialization error in reports"
git commit -m "Feature: Add new algorithm for OI analysis"
git commit -m "Update: Optimize settings for 500MB storage"
git commit -m "Docs: Add deployment guide"
```

### Step 5: Push to GitHub

```bash
git push origin main
```

You'll see:
```
Enumerating objects: ...
Writing objects: ...
To https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
   abc1234..xyz5678  main -> main
```

✅ **Done! Changes are on GitHub**

---

## 🌐 SCENARIO 2: Update PythonAnywhere After Push

Now update the live website on PythonAnywhere.

### Step 1: Open PythonAnywhere Bash Console

1. Go to: https://www.pythonanywhere.com
2. Click: **Consoles** tab
3. Click: **Start a new Bash console** (or use existing one)

### Step 2: Navigate to Project & Pull Latest Code

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
```

You'll see:
```
remote: Counting objects: 3, done.
Updating abc1234..xyz5678
Fast-forward
 dashboard/views.py | 10 +++++-----
 1 file changed, 5 insertions(+), 5 deletions(-)
```

✅ **Latest code is now on PythonAnywhere**

### Step 3: Activate Virtual Environment

```bash
workon optionchain
```

Your bash prompt will change:
```
(optionchain) 16:30 ~ $
```

### Step 4: If You Changed Django Settings or Added Packages

```bash
# Install any new packages (if requirements.txt changed)
# pip install -r requirements.txt

# Run migrations (if you added database models)
python manage.py migrate

# Re-collect static files
python manage.py collectstatic --noinput
```

### Step 5: Reload Web App

Go to PythonAnywhere **Web** tab and click the green **RELOAD** button.

Wait 10-15 seconds...

✅ **Your website is now updated!**

---

## 🚀 QUICK UPDATE COMMANDS

### If You Only Changed Python Code (No Migrations, No Static Files)

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# Then just click RELOAD in Web tab
```

### If You Changed Django Settings or Views

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Then click RELOAD in Web tab
```

### If You Added New Database Model

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py migrate
python manage.py collectstatic --noinput
# Then click RELOAD in Web tab
```

### Full Update (Do Everything)

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click RELOAD in Web tab.

---

## ⚡ COPY-PASTE TEMPLATES

### Template 1: Local - Make & Commit Change

```bash
# Local machine
git add -A
git commit -m "Your message here"
git push origin main
```

### Template 2: PythonAnywhere - Quick Update

```bash
# In PythonAnywhere Bash Console
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
```

Then click RELOAD button in Web tab.

### Template 3: PythonAnywhere - Full Update

```bash
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo "✅ Update complete! Click RELOAD in Web tab now"
du -sh .
```

---

## 📊 COMMON CHANGE TYPES

### Change Type 1: Bug Fix in Views/Algorithm

**Files changed**: `dashboard/views.py`, `dashboard/algorithms/*.py`

```bash
# Local
git add -A
git commit -m "Fix: bug description"
git push origin main

# PythonAnywhere
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
# Just click RELOAD (no migrations needed)
```

### Change Type 2: New Settings/Configuration

**Files changed**: `optionchain_project/settings.py`

```bash
# Local
git add -A
git commit -m "Update: settings for feature"
git push origin main

# PythonAnywhere
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Click RELOAD
```

### Change Type 3: New Database Model

**Files changed**: `dashboard/models.py` + new migration

```bash
# Local
git add -A
git commit -m "Add: new model for feature"
git push origin main

# PythonAnywhere
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py migrate
python manage.py collectstatic --noinput
# Click RELOAD
```

### Change Type 4: Frontend/CSS Changes

**Files changed**: `dashboard/templates/*.html`, `static/css/*.css`

```bash
# Local
git add -A
git commit -m "UI: improved layout"
git push origin main

# PythonAnywhere
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
python manage.py collectstatic --noinput
# Click RELOAD
```

### Change Type 5: New Python Packages

**Files changed**: `requirements.txt`

```bash
# Local
git add requirements.txt
git commit -m "Add: new package for feature"
git push origin main

# PythonAnywhere
cd ~/OptionChain-Analyser_CSV
git pull origin main
workon optionchain
pip install -r requirements.txt
python manage.py collectstatic --noinput
# Click RELOAD
```

---

## 🆘 TROUBLESHOOTING

### Problem: Git says "nothing to commit"

This means no changes were made. Add files explicitly:

```bash
git add dashboard/views.py
git status  # Check if it shows changes
git commit -m "message"
git push origin main
```

### Problem: Git says "Permission denied"

Add SSH key to GitHub:
1. Generate key: `ssh-keygen -t ed25519 -C "your@email.com"`
2. Add to GitHub: https://github.com/settings/ssh
3. Or use HTTPS instead of SSH

### Problem: "fatal: not a git repository"

Make sure you're in project directory:
```bash
cd ~/OptionChain-Analyser_CSV
git status
```

### Problem: PythonAnywhere gives 500 error after update

```bash
# Check what went wrong
tail -f /var/log/udayoption.pythonanywhere_com_error.log

# Fix and re-collect
python manage.py collectstatic --noinput
# Then RELOAD
```

### Problem: Migration fails

```bash
# Check migrations
python manage.py showmigrations

# Reset if needed (careful!)
python manage.py migrate --fake-initial
```

---

## 📋 STEP-BY-STEP EXAMPLE

**Scenario**: You fixed a bug in the Decimal serialization

### Local Machine

```bash
# 1. Edit file
# (Edit dashboard/views.py to fix bug)

# 2. Check changes
git status

# 3. Add changes
git add dashboard/views.py

# 4. Verify they're staged
git status
# Should show: "Changes to be committed: dashboard/views.py"

# 5. Commit
git commit -m "Fix: Decimal serialization in report generation"

# 6. Push to GitHub
git push origin main

# Result: You should see "main -> main" message
```

### PythonAnywhere

```bash
# 1. Open Bash Console in PythonAnywhere
# 2. Navigate to project
cd ~/OptionChain-Analyser_CSV

# 3. Pull latest code from GitHub
git pull origin main
# Result: Should show file changes

# 4. Activate virtual environment
workon optionchain

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Go to Web tab and click RELOAD

# 7. Test at https://udayoption.pythonanywhere.com
```

---

## 🎯 BEST PRACTICES

✅ **Do**:
- Commit frequently with clear messages
- Pull before pushing
- Test locally before pushing
- Check `git status` before committing

❌ **Don't**:
- Commit `.env` file (secrets exposed!)
- Commit large files (>10MB)
- Commit `db.sqlite3` (local database)
- Commit `staticfiles/` (auto-generated)

---

## 🔐 IMPORTANT: Never Commit These

```bash
# Already in .gitignore, but double-check:
# - .env (API keys!)
# - db.sqlite3 (local database)
# - staticfiles/ (auto-generated)
# - logs/ (auto-generated)
# - *.pyc (compiled Python)
# - __pycache__/ (cache)

# If accidentally committed:
git rm --cached .env
git commit -m "Remove .env file"
```

---

## 📞 QUICK REFERENCE

| Task | Command |
|------|---------|
| Check changes | `git status` |
| Add all | `git add -A` |
| Add specific | `git add file.py` |
| Commit | `git commit -m "msg"` |
| Push to GitHub | `git push origin main` |
| Pull from GitHub | `git pull origin main` |
| View history | `git log --oneline` |
| See what changed | `git diff` |
| Undo last commit | `git reset --soft HEAD~1` |
| Undo completely | `git reset --hard HEAD~1` |

---

**Remember**: Local changes → Git → GitHub → PythonAnywhere → RELOAD

✅ **That's the complete workflow!**
