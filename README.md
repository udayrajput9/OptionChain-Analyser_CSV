# 🎯 OptionChain-Analyser: AI-Powered Options Trading Intelligence

An intelligent options chain analysis platform that combines **20+ prediction algorithms** with **Claude AI reasoning** to deliver actionable daily trading insights for Indian equity options traders.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture & System Design](#architecture--system-design)
- [Installation & Setup](#installation--setup)
- [Usage Workflow](#usage-workflow)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Database Models](#database-models)
- [API Routes](#api-routes)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**OptionChain-Analyser** is a next-generation trading intelligence platform designed for NSE options traders. It processes intraday option chain snapshots and combines:

- **20 Prediction Algorithms** (10 ML + 10 Hedge Fund strategies)
- **3 Master Algorithms** (Titan Elite squeeze detector, Alpha-Omega OI matrix, Quantum Vega model)
- **Claude AI Super Brain** that synthesizes all signals into unified daily predictions
- **Continuous Learning System** that validates predictions and dynamically weights algorithms based on accuracy

**Use Case**: Upload daily option chain CSVs at different market times (9:10 AM, 1 PM, 3 PM), get AI-powered directional bias, price targets, and professional trading strategies—with the system learning from outcomes to improve accuracy daily.

---

## ✨ Key Features

### 📊 Option Chain Analysis
- **Multi-file uploads** - process 3 daily snapshots per stock at different time slots
- **Advanced parsing** - extracts Greeks, OI, volume, implied volatility, strike analysis
- **40+ market features** - derives comprehensive option microstructure metrics

### 🤖 20-Algorithm Ensemble
| Category | Count | Examples |
|----------|-------|----------|
| **ML Models** | 10 | Random Forest, XGBoost, LSTM, Transformer, Prophet, Monte Carlo, GARCH, LightGBM, SVM, Ensemble |
| **Hedge Fund Strategies** | 10 | Black-Scholes Greeks, Max Pain, PCR Analysis, OI Concentration, IV Skew, GEX, Delta Hedging, IV Term Structure, etc. |
| **Master Algorithms** | 3 | Titan Elite (Squeeze), Alpha-Omega (OI), Quantum Vega (Premium) |

### 🧠 Super Brain AI Orchestrator
- **Weighted voting** - each algorithm weighted by historical accuracy + confidence
- **Feature synthesis** - combines option microstructure + global macro signals
- **LLM integration** - Claude AI generates Hinglish reasoning for each daily prediction
- **Scenario analysis** - bull/base/bear cases with probabilities and targets
- **Confidence calibration** - learns whether predicted confidence matches actual accuracy

### 🌍 Global Market Context
Captures complete market backdrop including:
- **Indian Indices**: Nifty, Sensex, India VIX, Gift Nifty, FII/DII flows
- **Asian Markets**: Hang Seng, Nikkei, Shanghai Composite
- **US Markets**: Dow Jones, S&P 500, Nasdaq, sentiment classification
- **European Markets**: DAX, FTSE, CAC40
- **Macro Data**: Crude oil, USD-INR, Dollar Index (DXY)

### 📈 Outcome Tracking & Learning
- **Daily validation** - feed next-day actual close to validate all 20 predictions
- **Accuracy metrics** - tracks direction accuracy (70%), price accuracy (30%), error percentages
- **Dynamic weighting** - Super Brain learns algorithm reliability per stock
- **Persistent memory** - stores patterns, learnings, and confidence adjustments per stock

### 📱 Professional Dashboard & Reports
- **Dashboard** - stock overview, file counts, slot status tracking
- **Report View** - algo cards grid, master algorithms, intraday comparison, professional narrative
- **Prediction Detail** - Super Brain's signal, price targets, scenarios, key factors
- **Learning Report** - algorithm leaderboard, rolling accuracy trends
- **Professional Narrative** - auto-generated Hinglish strategy with market structure analysis, risk controls, tomorrow's price map

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2.9+ |
| **Database** | SQLite3 |
| **Data Processing** | Pandas, NumPy |
| **AI/LLM** | Anthropic Claude 3 Opus |
| **Frontend** | Bootstrap 5, Django Templates |
| **Environment** | python-dotenv |
| **Time Zone** | Asia/Kolkata (IST) |

---

## 🏗 Architecture & System Design

### Data Flow Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CSV UPLOAD & PARSING                                         │
│    NSE Option Chain CSV → Extract Greeks, OI, Strikes, Expiry   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. FEATURE EXTRACTION & MARKET CONTEXT                          │
│    - 40+ option chain micro features                            │
│    - Global macro data entry (Nifty, US, FII, crude, etc)      │
│    - Historical trend features                                  │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. PARALLEL ALGORITHM EXECUTION                                 │
│    ┌──────────────────────────────────────────────────────────┐ │
│    │ 10 ML Algorithms  │ 10 Hedge Fund Strategies │          │ │
│    │ + 3 Master Algos  │ (Each: signal, targets)  │          │ │
│    └──────────────────────────────────────────────────────────┘ │
│    Each producing: signal, price targets, confidence (0-100)    │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. SUPER BRAIN SYNTHESIS (Claude AI)                            │
│    - Load each algo's historical accuracy                       │
│    - Weighted voting: weight = accuracy × confidence            │
│    - Feature voting: option structure vote + macro vote         │
│    - LLM reasoning: generate Hinglish insight                   │
│    - Scenario analysis: bull/base/bear with probabilities       │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. REPORT GENERATION                                            │
│    - Professional narrative with strategy                       │
│    - Algo cards, master algorithms, intraday comparison         │
│    - Market structure analysis, risk controls                   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
        ┌──────────────────────────────────────────┐
        │ TRADER TAKES DECISION                    │
        └──────────────────────────────────────────┘
                             ↓
        ┌──────────────────────────────────────────┐
        │ NEXT DAY: OUTCOME FEED                   │
        │ Feed actual close price                  │
        └──────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. VALIDATION & LEARNING                                        │
│    - Validate 20 algo predictions vs actual                     │
│    - Track: direction correct, price in range, error %          │
│    - Update AlgoPerformanceMetrics (rolling 10-day accuracy)    │
│    - Update SuperBrainMemory with learnings                     │
│    - Reweight future predictions                                │
└─────────────────────────────────────────────────────────────────┘
```

### Ensemble Algorithm Voting

Each algorithm is a specialized expert:

```
Algorithm Returns:
├─ Signal: BULLISH / BEARISH / NEUTRAL
├─ Price Target: low, mid, high
├─ Confidence: 0-100%
├─ Breakdown: component-wise scoring
└─ Key Insight: reasoning

Super Brain Processing:
├─ Load Historical Metrics
│  └─ 10-day direction accuracy
│  └─ Confidence calibration
│  └─ Combined score
│
├─ Weighted Voting
│  ├─ Per-algorithm weight = (accuracy × confidence / 10000)
│  ├─ Vote aggregation
│  └─ Feature-level voting (option + macro)
│
├─ Confidence Calculation
│  └─ 48 + (score_magnitude × 0.32) + ((100 - disagreement) × 0.18)
│  └─ Result: 40-93% confidence range
│
└─ LLM Synthesis (Claude)
   ├─ Full context provided
   ├─ Hinglish reasoning generated
   ├─ 3 scenarios modeled
   └─ Key factors ranked
```

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Anthropic API key (for Claude)

### Step 1: Clone Repository
```bash
git clone https://github.com/udayrajput9/OptionChain-Analyser_CSV.git
cd optionchain_project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create `.env` file in project root:
```
ANTHROPIC_API_KEY=your_claude_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key
```

### Step 5: Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin panel
```

### Step 6: Create Stock Directories
```bash
mkdir stocks/TCS
mkdir stocks/ETERNAL
mkdir stocks/[YOUR_STOCK]
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 📖 Usage Workflow

### 1️⃣ Upload Option Chain CSV

**URL**: `/upload/`

- Select stock symbol (TCS, ETERNAL, etc.)
- Upload NSE/TradingView option chain CSV
- Or manually enter market context form data

**Supported CSV Format**:
```
# Downloaded: 18/4/2026, 12:45:04 pm
# Underlying: TCS
# Expiry: 25-APR-2026
# ATM: 3270

Strike,Call OI,Call Volume,Call IV,...,Put OI,Put Volume,Put IV,...
3230,12345,5000,18.5,...,54321,3000,19.2,...
3240,23456,7500,17.8,...,43210,4500,18.9,...
...
```

### 2️⃣ View Analysis Report

**URL**: `/report/<stock>/<date>/`

The system automatically:
- Parses option chain
- Derives all market features
- Runs 20 algorithms in parallel
- Compiles Super Brain prediction
- Renders professional report with:
  - 20 algo cards (signal, targets, confidence)
  - 3 master algorithms
  - Historical feature comparison
  - Intraday changes
  - Professional narrative strategy
  - Super Brain reasoning

### 3️⃣ Review Super Brain Prediction

**URL**: `/prediction/<stock>/<date>/`

See:
- Super Brain's signal + confidence
- Primary price targets
- 3 scenario analysis (bull/base/bear)
- Key decision factors ranked by impact
- Historical accuracy leaderboard
- Super Brain's per-stock learning memory

### 4️⃣ Feed Outcome (Next Day)

**URL**: `/outcome/<stock>/<date>/`

- Enter actual closing price from previous day
- System validates all 20 predictions
- Checks: direction correct? price in range?
- Updates algorithm accuracy metrics
- Super Brain learns and reweights

### 5️⃣ Review Learning Report

**URL**: `/learning-report/<stock>/<date>/`

- Algorithm leaderboard (sorted by accuracy)
- Correct vs wrong predictions
- Rolling 10-day accuracy trends
- Super Brain's learnings & improvements
- Confidence calibration insights

---

## 📁 Project Structure

```
optionchain_project/
│
├── manage.py                          # Django entry point
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
├── README.md                          # This file
│
├── optionchain_project/               # Django settings
│   ├── settings.py                    # Configuration
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI config
│   └── __init__.py
│
├── dashboard/                         # Main app
│   ├── models.py                      # DB models
│   │   ├── MarketContext              # Global market snapshot
│   │   ├── AlgoPredictionRecord       # Per-algo daily prediction
│   │   ├── AlgoPerformanceMetrics     # Rolling accuracy scorecard
│   │   ├── SuperBrainPredictionRecord # AI meta-prediction
│   │   └── SuperBrainMemory           # Persistent learning store
│   │
│   ├── views.py                       # View controllers
│   │   ├── DashboardView              # Stock overview
│   │   ├── UploadView                 # CSV upload
│   │   ├── ReportView                 # Main analysis (runs algos)
│   │   ├── PredictionView             # Super Brain detail
│   │   ├── OutcomeFeedView            # Outcome validation
│   │   └── LearningReportView         # Accuracy trends
│   │
│   ├── urls.py                        # Route definitions
│   ├── forms.py                       # Django forms
│   ├── apps.py                        # App config
│   │
│   ├── algorithms/                    # 20 algorithms
│   │   ├── ml_algorithms.py           # 10 ML models
│   │   ├── hedgefund_algorithms.py    # 10 HF strategies
│   │   ├── master_hf_algo.py          # 3 master algos
│   │   ├── prediction_engine.py       # Algo orchestrator
│   │   ├── super_brain.py             # Claude AI integration
│   │   ├── core.py                    # Feature derivation (40+ features)
│   │   └── __init__.py
│   │
│   ├── utils/                         # Utilities
│   │   ├── data_loader.py             # CSV file management
│   │   ├── data_cleaner.py            # CSV parsing & feature extraction
│   │   ├── performance_tracker.py     # Accuracy metrics calculation
│   │   ├── report_builder.py          # Narrative report generation
│   │   └── __init__.py
│   │
│   ├── templates/dashboard/           # HTML templates
│   │   ├── base.html                  # Base layout
│   │   ├── index.html                 # Dashboard
│   │   ├── upload.html                # Upload form
│   │   ├── report.html                # Main report
│   │   ├── prediction.html            # Super Brain detail
│   │   ├── outcome_feed.html          # Outcome form
│   │   ├── learning_report.html       # Leaderboard
│   │   └── components/algo_card.html  # Reusable algo card
│   │
│   ├── migrations/                    # DB migrations
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   └── __init__.py
│
├── stocks/                            # CSV data storage
│   ├── TCS/
│   │   ├── 1_TCS_OptionChain.csv
│   │   ├── 2_TCS_OptionChain.csv
│   │   └── ...
│   │
│   └── ETERNAL/
│       ├── 1_ETERNAL_OptionChain.csv
│       └── ...
│
└── static/                            # Static assets
    └── (Bootstrap CSS, images, etc.)
```

---

## 🧠 How It Works

### Step 1: Parse Option Chain
Extracts from CSV:
- Option Greeks (Delta, Gamma, Vega, Theta)
- Open Interest (OI) by strike
- Volume, Implied Volatility (IV)
- Bid-ask spreads, Greeks trends

### Step 2: Derive 40+ Market Features

**Option Microstructure:**
- Net Delta (dealer long/short positioning)
- Max Pain (options expiry gravity level)
- Call/Put walls (OI concentration)
- Put-Call Ratio (OI & volume)
- IV Skew (volatility smile profile)
- Gamma imbalance (dealer hedging need)
- Support/resistance strength
- Liquidity score
- Delta flow (near-ATM pressure)

**Global Macro Context:**
- Gift Nifty bias (next-day sentiment)
- US market sentiment + performance
- Asia composite (Hang Seng + Nikkei + Shanghai)
- Europe performance (DAX + FTSE + CAC40)
- FII/DII flow direction
- Currency impact (USD-INR)
- Dollar strength (DXY)
- Crude correlation

### Step 3: Run 20 Algorithms in Parallel

Each algorithm independently:
- Analyzes specific market aspect
- Produces directional signal (BULLISH/BEARISH/NEUTRAL)
- Calculates price target (low, mid, high)
- Assigns confidence (0-100%)
- Returns breakdown showing component scores

**Example - Max Pain Algorithm:**
```python
def max_pain_theory(ctx):
    """
    Max pain = strike where most options expire worthless
    Dealer positioning gravitates towards max pain
    Strong algorithmic target level
    """
    max_pain = ctx['summary']['max_pain']
    current = ctx['current_price']
    
    if current < max_pain - 50:
        signal = "BULLISH"  # Distance to max pain
    elif current > max_pain + 50:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"   # Already near max pain
    
    confidence = min(100, abs(current - max_pain) / 10)
    return {'signal': signal, 'confidence': confidence, ...}
```

### Step 4: Super Brain Orchestration (Claude AI)

```python
# Load historical accuracy for each algo
weights = {
    'Random Forest': metrics.combined_score * confidence / 10000,
    'Max Pain': metrics.combined_score * confidence / 10000,
    ...
}

# Weighted voting
bullish_votes = sum(w for algo, w in weights.items() if algo_signal == "BULLISH")
bearish_votes = sum(w for algo, w in weights.items() if algo_signal == "BEARISH")
net_vote = bullish_votes - bearish_votes

# Calculate final signal
score = net_vote * 24 + feature_vote * 0.62
final_signal = "BULLISH" if score > 18 else "BEARISH" if score < -18 else "NEUTRAL"

# Calculate confidence
confidence = 48 + abs(score) * 0.32 + (100 - disagreement) * 0.18

# Call Claude for Hinglish reasoning
prompt = f"""
Stock: {stock}
Price: {price}
Signal: {final_signal}
Confidence: {confidence}%
...
Generate Hinglish insight in 50 words. Then provide 3 scenarios: bull, base, bear.
"""
response = claude.generate(prompt)
```

### Step 5: Professional Report Generation

Auto-generates narrative with:
- Executive summary (10 algos bullish, 5 bearish, 5 neutral)
- Market structure analysis (support, resistance, max pain)
- Global context impact
- Trading strategy recommendation
- Risk controls & disclaimers
- Tomorrow's price map

### Step 6: Next Day Outcome Validation

When trader feeds actual close:
1. Check if direction was correct (BULLISH prediction → close up?)
2. Check if price stayed in target range
3. Calculate error percentage
4. Update AlgoPerformanceMetrics
5. Recalibrate confidence (did algo's confidence match accuracy?)
6. Update SuperBrainMemory with learnings
7. Adjust weights for next day's Super Brain voting

---

## 📊 Database Models

### MarketContext
Stores daily global market snapshot per (date, stock, time_slot):
```python
stock_symbol           # TCS, ETERNAL, etc
date                   # Trading date
context_slot           # MORNING_0910, MIDDAY_1300, CLOSE_1500
stock_open, high, low, close, volume
nifty_open, close, change, india_vix, gift_nifty
sensex_open, close, change
hang_seng, nikkei, shanghai (changes)
dow_jones, sp500, nasdaq (prev close + sentiment)
dax, ftse, cac40 (changes)
crude_oil_price, dollar_index_dxy, usd_inr
fii_data_net, dii_data_net
overall_market_sentiment
analyst_notes
```

### AlgoPredictionRecord
Daily prediction from each algorithm:
```python
date, stock_symbol, file_number
algo_name, algo_category (ML or HEDGE_FUND)
predicted_signal (BULLISH/BEARISH/NEUTRAL)
predicted_price_low, mid, high
confidence_score (0-100)
full_algo_output (JSON - complete breakdown)

# Filled next day:
actual_close_price
actual_signal
direction_correct, price_in_range, price_error_pct
outcome_fed_at
```

### AlgoPerformanceMetrics
Rolling scorecard per algorithm per stock:
```python
algo_name, stock_symbol
direction_accuracy (% correct)
price_accuracy (% in range)
combined_score (weighted)
rolling_10day_accuracy
confidence_calibration
```

### SuperBrainPredictionRecord
Daily AI meta-prediction:
```python
date, stock_symbol
input_market_context (JSON of MarketContext)
input_algo_results (JSON of 20 algo outputs)

super_brain_signal
super_brain_price_target, price_low, price_high
super_brain_confidence (40-93%)
super_brain_reasoning (string)

bull_case, base_case, bear_case (JSON with probs & targets)
super_brain_key_factors (top 5 factors ranked)

# Filled next day:
actual_close_price
direction_correct, score, outcome_fed_at
```

### SuperBrainMemory
Persistent learning store per stock:
```python
stock_symbol
pattern_library (JSON - historically successful patterns)
algo_trust_weights (JSON - per-algo reliability)
market_context_patterns (JSON - macro pattern recognition)
accuracy_history (JSON timeline)
```

---

## 🌐 API Routes

| Method | URL | View | Purpose |
|--------|-----|------|---------|
| GET | `/` | DashboardView | Show all stocks, file counts, slot status |
| GET | `/upload/` | UploadView | CSV upload form |
| POST | `/upload/` | UploadView | Process CSV or market context form |
| POST | `/stock/<stock>/reset/` | StockResetView | Clear all stock files & data |
| POST | `/stock/<stock>/delete/` | StockDeleteView | Delete stock folder |
| GET | `/report/<stock>/<date>/` | ReportView | **Main page** - run algos & show report |
| GET | `/prediction/<stock>/<date>/` | PredictionView | Super Brain prediction detail |
| GET | `/outcome/<stock>/<date>/` | OutcomeFeedView | Feed actual close form |
| POST | `/outcome/<stock>/<date>/` | OutcomeFeedView | Validate predictions |
| GET | `/learning-report/<stock>/<date>/` | LearningReportView | Algorithm leaderboard |

---

## 🔄 Algorithm Execution Order

1. **Feature Derivation** (40+ metrics from option chain)
2. **ML Algorithms** (Random Forest, XGBoost, LSTM, Prophet, etc.) - parallel
3. **Hedge Fund Strategies** (Max Pain, PCR, OI, Greeks, etc.) - parallel
4. **Master Algorithms** (Squeeze, OI, Vega) - parallel
5. **Compile Results** (20 outputs collected)
6. **Super Brain Weighting** (load accuracy metrics)
7. **Weighted Voting** (net sentiment calculation)
8. **LLM Synthesis** (Claude generates reasoning)
9. **Report Generation** (professional narrative)
10. **Database Storage** (all predictions saved)
11. **Render View** (HTML template with all data)

---

## 📚 Key Insights & Learning Mechanisms

### Outcome Validation
Every prediction is validated:
```
Direction Check:    BULLISH → Close up? / BEARISH → Close down?
Price Check:        actual_close between predicted_low and predicted_high?
Error Calculation: |actual_close - predicted_target| / actual_close × 100%
```

### Dynamic Algorithm Weighting
```
Each day:
1. Calculate algo's 10-day rolling direction accuracy
2. Check confidence calibration (did predictions match confidence?)
3. Update weight = (accuracy × recent_performance) × (stock_specific)
4. Super Brain uses updated weights next day
```

### Super Brain Learning
```
Pattern tracking per stock:
- When does max pain theory work well?
- When do ML models outperform hedge fund strategies?
- What market conditions favor which algorithm?
- Store in SuperBrainMemory for future use
```

---

## 🚀 Future Enhancements

- [ ] Real-time option chain streaming integration
- [ ] Advanced pattern recognition using additional ML
- [ ] Multi-stock portfolio correlation analysis
- [ ] Risk management alerts & position sizing
- [ ] Integration with trading venue APIs
- [ ] Mobile app for on-the-go monitoring
- [ ] Extended backtesting framework
- [ ] Options Greeks hedging recommendations
- [ ] Sector-wise analysis & rotation signals
- [ ] Event impact modeling (earnings, RBI, etc.)

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -am 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open Pull Request

---

## 📄 License

This project is released under the MIT License - see LICENSE file for details.

---

## 🙋 Support & Questions

For questions, issues, or suggestions:
- Open an GitHub issue on the repository
- Email: support@optionchainanalyser.com
- Check the FAQ in project wiki

---

## 📌 Important Notes

### Trading Disclaimer
⚠️ **IMPORTANT**: This tool is for educational and informational purposes only. It is not financial advice. Past performance doesn't guarantee future results. Options trading involves risk including loss of capital. Always:
- Do your own research
- Consult with a financial advisor
- Use appropriate position sizing
- Implement proper risk management
- Understand option pricing & Greeks

### API Credits
- Claude AI: Anthropic (requires API key & credits)
- Option data: User-provided NSE CSV exports

### Performance Note
- System requires Anthropic API key for Claude integration
- Processing time ~2-5 seconds per report (depending on API latency)
- Recommended for daily (not intraday) multiple uploads

---

**Version**: 1.0.0  
**Last Updated**: April 19, 2026  
**Maintained by**: OptionChain-Analyser Development Team

---

Happy Trading! 🎯📈
