#!/bin/bash
# PythonAnywhere Quick Deploy Script for udayoption
# Copy and paste each section into PythonAnywhere Bash Console
# Website: udayoption.pythonanywhere.com

echo "=== OptionChain-Analyser PythonAnywhere Deployment ==="
echo "Username: udayoption"
echo "Website: https://udayoption.pythonanywhere.com"
echo ""

# ============================================================
# SECTION 1: Clone Repository
# ============================================================
echo "STEP 1: Cloning Repository..."
cd ~
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd OptionChain-Analyser_CSV
echo "✓ Repository cloned!"

# ============================================================
# SECTION 2: Create Virtual Environment
# ============================================================
echo ""
echo "STEP 2: Creating Virtual Environment..."
mkvirtualenv --python=/usr/bin/python3.10 optionchain
workon optionchain
pip install --upgrade pip setuptools wheel
echo "✓ Virtual environment created!"

# ============================================================
# SECTION 3: Install Dependencies
# ============================================================
echo ""
echo "STEP 3: Installing Python Packages..."
pip install Django==4.2.9
pip install gunicorn==21.2.0
pip install whitenoise==6.5.0
pip install psycopg2-binary==2.9.9
pip install pandas==2.1.4
pip install numpy==1.24.3
pip install anthropic==0.7.1
pip install python-dotenv==1.0.0
echo "✓ All packages installed!"

# ============================================================
# SECTION 4: Database Setup
# ============================================================
echo ""
echo "STEP 4: Setting up Database..."
cd ~/OptionChain-Analyser_CSV
python manage.py migrate
echo "✓ Database migrations completed!"

# ============================================================
# SECTION 5: Create Directories
# ============================================================
echo ""
echo "STEP 5: Creating Directories..."
mkdir -p ~/OptionChain-Analyser_CSV/stocks/TCS
mkdir -p ~/OptionChain-Analyser_CSV/stocks/ETERNAL
mkdir -p ~/OptionChain-Analyser_CSV/logs
echo "✓ Directories created!"

# ============================================================
# SECTION 6: Collect Static Files
# ============================================================
echo ""
echo "STEP 6: Collecting Static Files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected!"

# ============================================================
# SECTION 7: Create .env File
# ============================================================
echo ""
echo "STEP 7: Creating .env File..."
cat > ~/OptionChain-Analyser_CSV/.env << 'ENVEOF'
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
DEBUG=False
SECRET_KEY=django-insecure-your-secret-key-here-make-it-long-and-random
PYTHONANYWHERE=True
ENVEOF

echo "✓ .env file created! (Edit it with your API key)"
echo ""
echo "Edit .env file now:"
echo "  nano ~/OptionChain-Analyser_CSV/.env"
echo ""
echo "Replace: sk-ant-YOUR_KEY_HERE with your actual Anthropic API key"
echo "Then: Ctrl+X, Y, Enter to save"

# ============================================================
# FINAL STATUS
# ============================================================
echo ""
echo "=============================================="
echo "✓ DEPLOYMENT SETUP COMPLETE!"
echo "=============================================="
echo ""
echo "NEXT STEPS:"
echo "1. Edit .env file and add your Anthropic API key"
echo "   $ nano ~/OptionChain-Analyser_CSV/.env"
echo ""
echo "2. Create superuser (admin):"
echo "   $ cd ~/OptionChain-Analyser_CSV"
echo "   $ python manage.py createsuperuser"
echo ""
echo "3. Go to PythonAnywhere Web Dashboard:"
echo "   - Click 'Web' tab"
echo "   - Add new web app"
echo "   - Choose Manual Configuration + Python 3.10"
echo "   - Set Virtualenv to: /home/udayoption/.virtualenvs/optionchain"
echo "   - Edit WSGI file (see PYTHONANYWHERE_DEPLOYMENT.md)"
echo "   - Add Static files mapping: /static/ -> /home/udayoption/OptionChain-Analyser_CSV/staticfiles"
echo "   - Click RELOAD"
echo ""
echo "4. Visit: https://udayoption.pythonanywhere.com"
echo ""
echo "=============================================="
