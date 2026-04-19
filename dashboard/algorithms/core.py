from __future__ import annotations

from statistics import mean


def clamp(value, low=-100.0, high=100.0):
    return max(low, min(high, float(value)))


def safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _signal_from_score(score):
    if score >= 20:
        return "BULLISH"
    if score <= -20:
        return "BEARISH"
    return "NEUTRAL"


def derive_market_features(ctx):
    summary = ctx.get('summary', {})
    market = ctx.get('market_context', {})
    history = ctx.get('historical_features', {})
    context_slot = market.get('context_slot', 'CLOSE_1500')
    slot_global_emphasis = {
        'MORNING_0910': 1.18,
        'MIDDAY_1300': 1.0,
        'CLOSE_1500': 0.84,
    }.get(context_slot, 1.0)
    slot_option_emphasis = {
        'MORNING_0910': 0.88,
        'MIDDAY_1300': 1.0,
        'CLOSE_1500': 1.18,
    }.get(context_slot, 1.0)
    slot_reliability_bonus = {
        'MORNING_0910': 0.0,
        'MIDDAY_1300': 4.0,
        'CLOSE_1500': 8.0,
    }.get(context_slot, 0.0)
    price = safe_float(ctx.get('current_price'))
    max_pain = safe_float(summary.get('max_pain'), price)
    call_wall = safe_float(summary.get('highest_call_oi_strike'), price)
    put_wall = safe_float(summary.get('highest_put_oi_strike'), price)
    pcr_oi = safe_float(summary.get('pcr_oi'), 1.0)
    pcr_volume = safe_float(summary.get('pcr_volume'), 1.0)
    net_delta = safe_float(summary.get('net_delta'))
    iv_skew = safe_float(summary.get('iv_skew'))
    atm_iv = safe_float(summary.get('atm_iv'))
    near_atm_pcr = safe_float(summary.get('near_atm_pcr_volume'), pcr_volume)
    near_atm_delta_flow = safe_float(summary.get('near_atm_delta_flow'))
    gamma_imbalance = safe_float(summary.get('near_atm_gamma_imbalance'))
    support_strength = safe_float(summary.get('support_strength'))
    resistance_strength = safe_float(summary.get('resistance_strength'))
    put_wall_distance_pct = safe_float(summary.get('put_wall_distance_pct'))
    call_wall_distance_pct = safe_float(summary.get('call_wall_distance_pct'))
    time_value_skew = safe_float(summary.get('time_value_skew'))
    liquidity_score = safe_float(summary.get('liquidity_score'), 50.0)
    downside_iv_premium = safe_float(summary.get('downside_iv_premium'))

    support_gap = ((price - put_wall) / price) * 100 if price else 0.0
    resistance_gap = ((call_wall - price) / price) * 100 if price else 0.0
    wall_balance = clamp((resistance_gap - support_gap) * 8 * slot_option_emphasis)
    max_pain_bias = clamp((((max_pain - price) / price) * 600 if price else 0.0) * slot_option_emphasis)
    delta_bias = clamp(net_delta * 2.2 * slot_option_emphasis)
    pcr_bias = clamp(((pcr_oi - 1.0) * 70 + (pcr_volume - 1.0) * 35) * slot_option_emphasis)
    iv_skew_bias = clamp(iv_skew * 12 * slot_option_emphasis)
    near_atm_pressure_bias = clamp(((near_atm_pcr - 1.0) * 85 + near_atm_delta_flow * 140) * slot_option_emphasis)
    support_strength_bias = clamp((support_strength - resistance_strength) * 14 * slot_option_emphasis)
    wall_risk_bias = clamp((call_wall_distance_pct - put_wall_distance_pct) * 8 * slot_option_emphasis)
    time_value_bias = clamp(-time_value_skew * 2.4 * slot_option_emphasis)
    gamma_bias = clamp(gamma_imbalance * 45 * slot_option_emphasis)
    liquidity_bias = clamp((liquidity_score - 65.0) * 1.4 * slot_option_emphasis, -45, 45)
    downside_hedging_bias = clamp(-downside_iv_premium * 7 * slot_option_emphasis)
    vol_regime = clamp(
        (history.get('iv_trend_pct', 0.0) * -1.5)
        + ((18 - atm_iv) * 1.5)
        + history.get('premium_skew_trend', 0.0) * -0.6
    )

    gift_nifty = safe_float(market.get('gift_nifty_next_day_indication'))
    nifty_close = safe_float(market.get('nifty_close'))
    gift_bias = clamp((((gift_nifty - nifty_close) / nifty_close) * 4000 if nifty_close else 0.0) * slot_global_emphasis)
    fii_bias = clamp(safe_float(market.get('fii_data_net')) / 40.0)
    dii_bias = clamp(safe_float(market.get('dii_data_net')) / 60.0)
    us_sentiment = {
        'STRONG_BULLISH': 28,
        'BULLISH': 12,
        'NEUTRAL': 0,
        'BEARISH': -12,
        'STRONG_BEARISH': -28,
    }.get(market.get('us_market_sentiment'), 0)
    asia_bias = clamp(
        safe_float(market.get('hangseng_change_points')) / 45.0
        + safe_float(market.get('nikkei_change_points')) / 70.0
        + safe_float(market.get('shanghai_composite_change')) * 18.0
    ) * slot_global_emphasis
    europe_bias = clamp(
        safe_float(market.get('dax_change_points')) / 18.0
        + safe_float(market.get('ftse_change_points')) / 10.0
        + safe_float(market.get('cac40_change_points')) / 15.0
    ) * slot_global_emphasis
    crude_bias = clamp((85.0 - safe_float(market.get('crude_oil_price'), 85.0)) * 1.2 * slot_global_emphasis)
    dxy_bias = clamp((103.5 - safe_float(market.get('dollar_index_dxy'), 103.5)) * 5.5 * slot_global_emphasis)
    usd_inr_bias = clamp((84.2 - safe_float(market.get('usd_inr'), 84.2)) * 7.5 * slot_global_emphasis)
    india_vix = safe_float(market.get('india_vix'), 18.0)
    volatility_risk_bias = clamp((18.0 - india_vix) * 2.6 * (0.85 + 0.15 * slot_global_emphasis))
    currency_oil_bias = clamp(crude_bias + dxy_bias * 0.55 + usd_inr_bias * 0.45)
    flow_balance_bias = clamp(fii_bias * 0.75 + dii_bias * 0.35)
    global_macro_bias = clamp(
        gift_bias * 0.28
        + us_sentiment * 0.22
        + asia_bias * 0.18
        + europe_bias * 0.14
        + currency_oil_bias * 0.10
        + volatility_risk_bias * 0.08
    )
    trend_bias = clamp(history.get('price_trend_pct', 0.0) * 35)
    momentum_bias = clamp(history.get('delta_trend', 0.0) * 8 + history.get('delta_flow_trend', 0.0) * 140)
    summary_signal_fields = [
        atm_iv, pcr_volume, pcr_oi, net_delta, iv_skew, near_atm_pcr, near_atm_delta_flow,
        support_strength, resistance_strength, liquidity_score, downside_iv_premium,
    ]
    market_signal_fields = [
        gift_nifty, nifty_close, fii_bias, dii_bias, us_sentiment, asia_bias, europe_bias,
        crude_bias, dxy_bias, usd_inr_bias, india_vix,
    ]
    completeness = sum(
        1 for value in summary_signal_fields + market_signal_fields
        if abs(safe_float(value, 0.0)) > 0
    )
    data_quality = max(
        35.0,
        min(95.0, 38.0 + history.get('history_count', 0) * 6.5 + completeness * 1.2 + liquidity_score * 0.08 + slot_reliability_bonus)
    )
    expected_move_pct = max(0.8, min(4.5, atm_iv / 12 if atm_iv else 1.5))

    return {
        'price': price,
        'summary': summary,
        'market': market,
        'history': history,
        'context_slot': context_slot,
        'slot_global_emphasis': slot_global_emphasis,
        'slot_option_emphasis': slot_option_emphasis,
        'wall_balance': wall_balance,
        'max_pain_bias': max_pain_bias,
        'delta_bias': delta_bias,
        'pcr_bias': pcr_bias,
        'iv_skew_bias': iv_skew_bias,
        'near_atm_pressure_bias': near_atm_pressure_bias,
        'support_strength_bias': support_strength_bias,
        'wall_risk_bias': wall_risk_bias,
        'time_value_bias': time_value_bias,
        'gamma_bias': gamma_bias,
        'liquidity_bias': liquidity_bias,
        'downside_hedging_bias': downside_hedging_bias,
        'vol_regime': vol_regime,
        'gift_bias': gift_bias,
        'fii_bias': fii_bias,
        'dii_bias': dii_bias,
        'us_sentiment_bias': us_sentiment,
        'asia_bias': asia_bias,
        'europe_bias': europe_bias,
        'currency_oil_bias': currency_oil_bias,
        'volatility_risk_bias': volatility_risk_bias,
        'flow_balance_bias': flow_balance_bias,
        'global_macro_bias': global_macro_bias,
        'trend_bias': trend_bias,
        'momentum_bias': momentum_bias,
        'data_quality': data_quality,
        'expected_move_pct': expected_move_pct,
    }


def build_algorithm_output(ctx, config):
    features = ctx['derived_features']
    weights = config['weights']
    contributions = {}
    score = 0.0
    for feature_name, weight in weights.items():
        contribution = features.get(feature_name, 0.0) * weight
        contributions[feature_name] = round(contribution, 2)
        score += contribution

    score = clamp(score)
    signal = _signal_from_score(score)
    price = features['price']
    move_pct = features['expected_move_pct'] * config.get('range_multiplier', 1.0)
    directional_shift = (score / 100.0) * config.get('target_multiplier', 1.0) * move_pct
    target = price * (1 + directional_shift / 100.0)
    band = price * (move_pct / 100.0)
    low = min(target - band, target + band)
    high = max(target - band, target + band)
    confidence = max(
        38.0,
        min(
            94.0,
            40.0 + abs(score) * 0.42 + features['data_quality'] * 0.28
        ),
    )
    dominant = sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True)[:3]
    factor_labels = {
        'wall_balance': 'support-resistance wall balance',
        'max_pain_bias': 'max pain pull',
        'delta_bias': 'delta positioning',
        'pcr_bias': 'PCR imbalance',
        'iv_skew_bias': 'IV skew',
        'near_atm_pressure_bias': 'near-ATM flow pressure',
        'support_strength_bias': 'support vs resistance strength',
        'wall_risk_bias': 'wall proximity risk',
        'time_value_bias': 'time value skew',
        'gamma_bias': 'gamma imbalance',
        'liquidity_bias': 'option liquidity',
        'downside_hedging_bias': 'downside hedging premium',
        'vol_regime': 'volatility regime',
        'gift_bias': 'Gift Nifty signal',
        'fii_bias': 'FII flow',
        'dii_bias': 'DII flow',
        'us_sentiment_bias': 'US sentiment carry-over',
        'asia_bias': 'Asia market carry-over',
        'europe_bias': 'Europe market carry-over',
        'currency_oil_bias': 'currency and oil pressure',
        'volatility_risk_bias': 'India VIX risk tone',
        'flow_balance_bias': 'institutional balance',
        'global_macro_bias': 'global macro alignment',
        'trend_bias': 'historical price trend',
        'momentum_bias': 'delta momentum',
    }
    dominant_text = ", ".join(
        f"{factor_labels.get(name, name)} ({'+' if value >= 0 else ''}{round(value, 1)})"
        for name, value in dominant
    )
    insight_prefix = config.get('insight_prefix', config['algorithm_name'])
    insight = (
        f"{insight_prefix} score {round(score, 1)} hai. "
        f"Sabse strong drivers: {dominant_text}."
    )
    return {
        "algorithm_name": config['algorithm_name'],
        "category": config['category'],
        "signal": signal,
        "confidence": round(confidence, 2),
        "price_target_low": round(low, 2),
        "price_target_high": round(high, 2),
        "price_target_mid": round(target, 2),
        "key_insight": insight,
        "risk_level": config.get('risk_level', 'MEDIUM'),
        "supporting_data": {
            "score": round(score, 2),
            "feature_contributions": contributions,
            "history_count": features['history'].get('history_count', 0),
            "expected_move_pct": round(move_pct, 2),
        },
    }


def summarize_history(historical_snapshots):
    if not historical_snapshots:
        return {
            'history_count': 0,
            'price_trend_pct': 0.0,
            'iv_trend_pct': 0.0,
            'delta_trend': 0.0,
            'delta_flow_trend': 0.0,
            'premium_skew_trend': 0.0,
            'near_atm_pcr_trend': 0.0,
            'avg_pcr_volume': 1.0,
            'avg_atm_iv': 0.0,
        }

    prices = [safe_float(day['summary'].get('underlying_price')) for day in historical_snapshots if safe_float(day['summary'].get('underlying_price'))]
    ivs = [safe_float(day['summary'].get('atm_iv')) for day in historical_snapshots if safe_float(day['summary'].get('atm_iv'))]
    deltas = [safe_float(day['summary'].get('net_delta')) for day in historical_snapshots]
    pcrs = [safe_float(day['summary'].get('pcr_volume'), 1.0) for day in historical_snapshots]
    near_pcrs = [safe_float(day['summary'].get('near_atm_pcr_volume'), 1.0) for day in historical_snapshots]
    delta_flows = [safe_float(day['summary'].get('near_atm_delta_flow')) for day in historical_snapshots]
    premium_skews = [safe_float(day['summary'].get('downside_iv_premium')) for day in historical_snapshots]

    price_trend_pct = ((prices[-1] - prices[0]) / prices[0] * 100) if len(prices) >= 2 and prices[0] else 0.0
    iv_trend_pct = ((ivs[-1] - mean(ivs[:-1])) / mean(ivs[:-1]) * 100) if len(ivs) >= 3 and mean(ivs[:-1]) else 0.0
    delta_trend = (deltas[-1] - deltas[0]) if len(deltas) >= 2 else 0.0
    return {
        'history_count': len(historical_snapshots),
        'price_trend_pct': round(price_trend_pct, 3),
        'iv_trend_pct': round(iv_trend_pct, 3),
        'delta_trend': round(delta_trend, 3),
        'delta_flow_trend': round((delta_flows[-1] - delta_flows[0]) if len(delta_flows) >= 2 else 0.0, 5),
        'premium_skew_trend': round((premium_skews[-1] - mean(premium_skews[:-1])) if len(premium_skews) >= 3 else 0.0, 3),
        'near_atm_pcr_trend': round((near_pcrs[-1] - near_pcrs[0]) if len(near_pcrs) >= 2 else 0.0, 3),
        'avg_pcr_volume': round(mean(pcrs), 3) if pcrs else 1.0,
        'avg_atm_iv': round(mean(ivs), 3) if ivs else 0.0,
    }
