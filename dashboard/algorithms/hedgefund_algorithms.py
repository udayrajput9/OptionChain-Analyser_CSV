from .core import build_algorithm_output


HF_CONFIGS = [
    {
        "algorithm_name": "Black-Scholes Greeks Analysis",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.95,
        "target_multiplier": 0.9,
        "weights": {"delta_bias": 0.24, "near_atm_pressure_bias": 0.18, "gamma_bias": 0.16, "vol_regime": 0.10, "iv_skew_bias": 0.10, "wall_balance": 0.12, "trend_bias": 0.10},
    },
    {
        "algorithm_name": "Max Pain Theory",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.8,
        "target_multiplier": 0.8,
        "weights": {"max_pain_bias": 0.34, "wall_balance": 0.16, "support_strength_bias": 0.16, "gift_bias": 0.10, "trend_bias": 0.08, "delta_bias": 0.08, "global_macro_bias": 0.08},
    },
    {
        "algorithm_name": "PCR Contrarian Analysis",
        "category": "Hedge Fund",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.0,
        "target_multiplier": 0.95,
        "weights": {"pcr_bias": 0.28, "near_atm_pressure_bias": 0.18, "trend_bias": -0.12, "gift_bias": 0.08, "fii_bias": 0.08, "wall_balance": 0.10, "downside_hedging_bias": 0.16},
    },
    {
        "algorithm_name": "OI Concentration Analysis",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.95,
        "target_multiplier": 1.0,
        "weights": {"wall_balance": 0.28, "support_strength_bias": 0.22, "wall_risk_bias": 0.16, "max_pain_bias": 0.12, "delta_bias": 0.10, "pcr_bias": 0.06, "gift_bias": 0.06},
    },
    {
        "algorithm_name": "IV Skew Analysis",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.9,
        "target_multiplier": 0.9,
        "weights": {"iv_skew_bias": 0.24, "downside_hedging_bias": 0.28, "vol_regime": 0.14, "gift_bias": 0.08, "trend_bias": 0.06, "us_sentiment_bias": 0.08, "global_macro_bias": 0.12},
    },
    {
        "algorithm_name": "Gamma Exposure GEX Analysis",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.75,
        "target_multiplier": 0.6,
        "weights": {"gamma_bias": 0.26, "wall_balance": 0.18, "max_pain_bias": 0.14, "vol_regime": 0.14, "delta_bias": 0.12, "trend_bias": 0.06, "liquidity_bias": 0.10},
    },
    {
        "algorithm_name": "Unusual Options Activity Detector",
        "category": "Hedge Fund",
        "risk_level": "HIGH",
        "range_multiplier": 1.35,
        "target_multiplier": 1.15,
        "weights": {"delta_bias": 0.18, "near_atm_pressure_bias": 0.18, "pcr_bias": 0.08, "wall_balance": 0.10, "trend_bias": 0.08, "fii_bias": 0.10, "gift_bias": 0.10, "global_macro_bias": 0.10, "gamma_bias": 0.08},
    },
    {
        "algorithm_name": "Delta Hedging Flow Predictor",
        "category": "Hedge Fund",
        "risk_level": "MEDIUM",
        "range_multiplier": 1.05,
        "target_multiplier": 1.0,
        "weights": {"delta_bias": 0.24, "near_atm_pressure_bias": 0.20, "momentum_bias": 0.14, "wall_balance": 0.10, "gift_bias": 0.08, "trend_bias": 0.08, "gamma_bias": 0.10, "liquidity_bias": 0.06},
    },
    {
        "algorithm_name": "IV Term Structure Analysis",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 0.85,
        "target_multiplier": 0.75,
        "weights": {"vol_regime": 0.20, "volatility_risk_bias": 0.16, "iv_skew_bias": 0.08, "downside_hedging_bias": 0.18, "gift_bias": 0.08, "us_sentiment_bias": 0.10, "dii_bias": 0.08, "global_macro_bias": 0.12},
    },
    {
        "algorithm_name": "Theoretical Value Arbitrage Scanner",
        "category": "Hedge Fund",
        "risk_level": "LOW",
        "range_multiplier": 1.0,
        "target_multiplier": 1.0,
        "weights": {"iv_skew_bias": -0.16, "downside_hedging_bias": -0.18, "pcr_bias": -0.14, "time_value_bias": 0.18, "wall_balance": 0.10, "max_pain_bias": 0.08, "vol_regime": 0.12, "liquidity_bias": 0.12},
    },
]


def _runner(config):
    def run(ctx):
        return build_algorithm_output(ctx, config)

    return run


ALL_HF_ALGORITHMS = [_runner(config) for config in HF_CONFIGS]
