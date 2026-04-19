from .core import build_algorithm_output


ML_CONFIGS = [
    {
        "algorithm_name": "Random Forest Options Analyzer",
        "category": "ML",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.05,
        "target_multiplier": 0.95,
        "weights": {"delta_bias": 0.32, "near_atm_pressure_bias": 0.22, "pcr_bias": 0.14, "support_strength_bias": 0.14, "trend_bias": 0.10, "wall_balance": 0.08},
    },
    {
        "algorithm_name": "XGBoost IV Surface Predictor",
        "category": "ML",
        "risk_level": "HIGH",
        "range_multiplier": 1.2,
        "target_multiplier": 1.1,
        "weights": {"iv_skew_bias": 0.26, "downside_hedging_bias": 0.24, "vol_regime": 0.18, "global_macro_bias": 0.16, "gift_bias": 0.08, "wall_balance": 0.08},
    },
    {
        "algorithm_name": "LSTM Temporal Pattern Detector",
        "category": "ML",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.0,
        "target_multiplier": 1.0,
        "weights": {"trend_bias": 0.28, "momentum_bias": 0.24, "delta_bias": 0.16, "near_atm_pressure_bias": 0.16, "vol_regime": 0.10, "global_macro_bias": 0.06},
    },
    {
        "algorithm_name": "Transformer Attention Model",
        "category": "ML",
        "risk_level": "HIGH",
        "range_multiplier": 1.15,
        "target_multiplier": 1.05,
        "weights": {"wall_balance": 0.20, "delta_bias": 0.18, "near_atm_pressure_bias": 0.16, "global_macro_bias": 0.16, "liquidity_bias": 0.10, "gift_bias": 0.10, "fii_bias": 0.10},
    },
    {
        "algorithm_name": "Prophet Time Series Forecaster",
        "category": "ML",
        "risk_level": "LOW",
        "range_multiplier": 0.85,
        "target_multiplier": 0.75,
        "weights": {"trend_bias": 0.28, "max_pain_bias": 0.14, "global_macro_bias": 0.18, "flow_balance_bias": 0.12, "gift_bias": 0.10, "us_sentiment_bias": 0.10, "vol_regime": 0.08},
    },
    {
        "algorithm_name": "Monte Carlo Simulation Engine",
        "category": "ML",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.35,
        "target_multiplier": 0.85,
        "weights": {"trend_bias": 0.16, "vol_regime": 0.16, "gamma_bias": 0.18, "global_macro_bias": 0.12, "gift_bias": 0.10, "max_pain_bias": 0.12, "wall_balance": 0.16},
    },
    {
        "algorithm_name": "GARCH Volatility Forecaster",
        "category": "ML",
        "risk_level": "LOW",
        "range_multiplier": 0.95,
        "target_multiplier": 0.9,
        "weights": {"vol_regime": 0.24, "volatility_risk_bias": 0.18, "downside_hedging_bias": 0.16, "iv_skew_bias": 0.10, "trend_bias": 0.10, "global_macro_bias": 0.12, "us_sentiment_bias": 0.10},
    },
    {
        "algorithm_name": "LightGBM Options Mispricing Detector",
        "category": "ML",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.1,
        "target_multiplier": 1.1,
        "weights": {"pcr_bias": 0.18, "near_atm_pressure_bias": 0.18, "time_value_bias": 0.16, "liquidity_bias": 0.12, "iv_skew_bias": 0.12, "wall_balance": 0.12, "delta_bias": 0.12},
    },
    {
        "algorithm_name": "SVM Regime Classifier",
        "category": "ML",
        "risk_level": "MEDIUM",
        "range_multiplier": 0.9,
        "target_multiplier": 0.7,
        "weights": {"vol_regime": 0.18, "trend_bias": 0.16, "global_macro_bias": 0.18, "gift_bias": 0.12, "us_sentiment_bias": 0.12, "downside_hedging_bias": 0.12, "max_pain_bias": 0.12},
    },
    {
        "algorithm_name": "Ensemble Meta-Learner",
        "category": "ML",
        "risk_level": "LOW",
        "range_multiplier": 1.0,
        "target_multiplier": 1.0,
        "weights": {"delta_bias": 0.14, "near_atm_pressure_bias": 0.14, "pcr_bias": 0.10, "support_strength_bias": 0.10, "wall_balance": 0.10, "trend_bias": 0.10, "global_macro_bias": 0.12, "vol_regime": 0.08, "gift_bias": 0.06, "fii_bias": 0.06},
    },
]


def _runner(config):
    def run(ctx):
        return build_algorithm_output(ctx, config)

    return run


ALL_ML_ALGORITHMS = [_runner(config) for config in ML_CONFIGS]
