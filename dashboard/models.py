from django.db import models

class MarketContext(models.Model):
    SLOT_0910 = 'MORNING_0910'
    SLOT_1300 = 'MIDDAY_1300'
    SLOT_1500 = 'CLOSE_1500'
    SLOT_CHOICES = [
        (SLOT_0910, '09:10 AM Global Pulse'),
        (SLOT_1300, '01:00 PM Midday Check'),
        (SLOT_1500, '03:00 PM Closing Setup'),
    ]

    date = models.DateField()
    context_slot = models.CharField(max_length=20, choices=SLOT_CHOICES, default=SLOT_1500)
    
    # === TARGET STOCK ===
    stock_symbol = models.CharField(max_length=20)
    stock_open = models.DecimalField(max_digits=10, decimal_places=2)
    stock_close = models.DecimalField(max_digits=10, decimal_places=2)
    stock_high = models.DecimalField(max_digits=10, decimal_places=2)
    stock_low = models.DecimalField(max_digits=10, decimal_places=2)
    stock_volume = models.BigIntegerField()
    
    # === INDIAN MARKET ===
    nifty_open = models.DecimalField(max_digits=10, decimal_places=2)
    nifty_close = models.DecimalField(max_digits=10, decimal_places=2)
    nifty_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    sensex_open = models.DecimalField(max_digits=10, decimal_places=2)
    sensex_close = models.DecimalField(max_digits=10, decimal_places=2)
    sensex_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    india_vix = models.DecimalField(max_digits=6, decimal_places=2)
    gift_nifty_prev_day = models.DecimalField(max_digits=10, decimal_places=2)  # prev day closing gift nifty
    
    # === ASIAN MARKETS (at Indian market close ~3:30 PM IST) ===
    hangseng_open = models.DecimalField(max_digits=10, decimal_places=2)
    hangseng_at_india_close = models.DecimalField(max_digits=10, decimal_places=2)
    hangseng_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    nikkei_open = models.DecimalField(max_digits=10, decimal_places=2)
    nikkei_at_india_open = models.DecimalField(max_digits=10, decimal_places=2)  # Japan opens before India
    nikkei_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    shanghai_composite_change = models.DecimalField(max_digits=8, decimal_places=2)
    
    # === US MARKETS ===
    dow_jones_prev_close = models.DecimalField(max_digits=10, decimal_places=2)
    sp500_prev_close = models.DecimalField(max_digits=10, decimal_places=2)
    nasdaq_prev_close = models.DecimalField(max_digits=10, decimal_places=2)
    dow_jones_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    us_market_sentiment = models.CharField(max_length=20, choices=[
        ('STRONG_BULLISH','Strong Bullish'),('BULLISH','Bullish'),
        ('NEUTRAL','Neutral'),('BEARISH','Bearish'),('STRONG_BEARISH','Strong Bearish')
    ])
    
    # === EUROPE MARKETS ===
    dax_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    ftse_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    cac40_change_points = models.DecimalField(max_digits=8, decimal_places=2)
    
    # === GIFT NIFTY (Next day morning indicator) ===
    gift_nifty_next_day_indication = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gift_nifty_next_premium = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # === ADDITIONAL CONTEXT ===
    crude_oil_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dollar_index_dxy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    usd_inr = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    fii_data_net = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # FII buying/selling in Cr
    dii_data_net = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    overall_market_sentiment = models.CharField(max_length=30)
    analyst_notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'stock_symbol', 'context_slot'], name='unique_market_context_per_slot')
        ]
        indexes = [models.Index(fields=['stock_symbol', 'date', 'context_slot'])]


class AlgoPredictionRecord(models.Model):
    """
    Har din ka 20 algorithms ka prediction store hoga.
    Next din actual outcome feed karne ke baad accuracy track hogi.
    """
    date = models.DateField()
    stock_symbol = models.CharField(max_length=20)
    file_number = models.IntegerField(default=1) # tracking file sequence number
    
    # ── Prediction Store ──
    algo_name = models.CharField(max_length=100)
    algo_category = models.CharField(max_length=20)  # "ML" or "HEDGE_FUND"
    predicted_signal = models.CharField(max_length=20)  # BULLISH/BEARISH/NEUTRAL
    predicted_price_low = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_price_high = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_price_target = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_score = models.FloatField()  # 0-100
    full_algo_output = models.JSONField()   # Complete dictionary store karo
    
    # ── Outcome Feed (next day update) ──
    actual_close_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_signal = models.CharField(max_length=20, null=True, blank=True)  # Actual: BULLISH/BEARISH
    direction_correct = models.BooleanField(null=True, blank=True)    # Signal sahi tha?
    price_in_range = models.BooleanField(null=True, blank=True)       # Price predicted range mein tha?
    price_error_pct = models.FloatField(null=True, blank=True)        # % error in price target
    outcome_fed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'stock_symbol', 'algo_name'], name='unique_algo_pred')
        ]
        indexes = [models.Index(fields=['stock_symbol', 'date'])]


class AlgoPerformanceMetrics(models.Model):
    """
    Har algorithm ki running accuracy — Super Brain isko use karta hai weights ke liye
    """
    stock_symbol = models.CharField(max_length=20)
    algo_name = models.CharField(max_length=100)
    
    total_predictions = models.IntegerField(default=0)
    correct_direction = models.IntegerField(default=0)
    price_range_hits = models.IntegerField(default=0)
    
    direction_accuracy = models.FloatField(default=50.0)   # %
    price_accuracy = models.FloatField(default=50.0)       # %
    combined_score = models.FloatField(default=50.0)       # weighted
    
    # Rolling accuracy (last 10 days)
    rolling_10_accuracy = models.FloatField(default=50.0)
    
    # Confidence calibration: kya algo jo confidence deta hai woh sahi hai?
    confidence_calibration_score = models.FloatField(default=1.0)  # 1.0 = perfect
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stock_symbol', 'algo_name'], name='unique_algo_metric')
        ]


class SuperBrainPredictionRecord(models.Model):
    """
    Super Brain (21st predictor) ka prediction + validation store
    """
    date = models.DateField()
    stock_symbol = models.CharField(max_length=20)
    
    # ── Super Brain Input Context ──
    total_algos_consulted = models.IntegerField(default=20)
    input_market_context = models.JSONField()
    input_algo_results = models.JSONField()         # Saare 20 algos ka output
    historical_performance_context = models.JSONField()  # Jo super brain ko diya
    
    # ── Super Brain's Own Prediction ──
    super_brain_signal = models.CharField(max_length=20)
    super_brain_price_low = models.DecimalField(max_digits=10, decimal_places=2)
    super_brain_price_high = models.DecimalField(max_digits=10, decimal_places=2)
    super_brain_price_target = models.DecimalField(max_digits=10, decimal_places=2)
    super_brain_confidence = models.FloatField()
    super_brain_reasoning = models.TextField()   # LLM ka full Hinglish reasoning
    super_brain_key_factors = models.JSONField() # Top 5 factors jo decision mein important the
    
    # ── Scenario Predictions ──
    bull_case = models.JSONField(null=True, blank=True)
    base_case = models.JSONField(null=True, blank=True)
    bear_case = models.JSONField(null=True, blank=True)
    
    # ── Validation (next day) ──
    actual_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    was_correct = models.BooleanField(null=True, blank=True)
    accuracy_score = models.FloatField(null=True, blank=True)   # 0-100
    
    # ── Learning Notes ──
    # Super Brain isko next iteration mein padha hoga
    post_analysis_hinglish = models.TextField(blank=True)  # "Kya galat hua, kya sahi hua"
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'stock_symbol'], name='unique_super_brain_pred')
        ]
        ordering = ['-date']


class SuperBrainMemory(models.Model):
    """
    Super Brain ka persistent memory — daily grow karta hai.
    Yahi isko "intelligent" banata hai over time.
    """
    stock_symbol = models.CharField(max_length=20, unique=True)
    
    # Compressed learnings (LLM se generate hoga)
    accumulated_learnings = models.TextField()        # Hinglish mein distilled wisdom
    pattern_library = models.JSONField(default=dict)  # {pattern: outcome} history
    algo_trust_weights = models.JSONField(default=dict)  # Dynamic weights per algo
    market_context_patterns = models.JSONField(default=dict)
    
    total_days_learned = models.IntegerField(default=0)
    accuracy_history = models.JSONField(default=list)  # [{"date": ..., "accuracy": ...}]
    
    last_updated = models.DateTimeField(auto_now=True)
