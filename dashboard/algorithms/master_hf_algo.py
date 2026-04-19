def run_institutional_squeeze_model(ctx):
    """
    Titan Elite: Institutional Net-Gamma & Volatility Squeeze Model
    Calculates a directional velocity score (-100 to +100) using real option chain greeks
    and available institutional flow metrics.
    """
    summary = ctx.get('summary', {})
    mkt = ctx.get('market_context', {})
    cp = ctx.get('current_price', 0)
    
    net_delta = summary.get('net_delta', 0)
    delta_score = min(max((net_delta / 1000) * 10, -35), 35)
    near_delta_flow = summary.get('near_atm_delta_flow', 0)
    flow_micro_score = min(max(near_delta_flow * 220, -18), 18)
    
    iv_skew = summary.get('iv_skew', 0)
    iv_score = min(max((iv_skew * 10), -25), 25)
    
    max_pain = summary.get('max_pain', cp)
    pain_diff_pct = ((max_pain - cp) / cp) * 100 if cp else 0
    pain_score = min(max(pain_diff_pct * 5, -20), 20)
    
    fii = float(mkt.get('fii_data_net') or 0)
    flow_score = min(max((fii / 2000) * 20, -20), 20)
    support_strength = float(summary.get('support_strength') or 0)
    resistance_strength = float(summary.get('resistance_strength') or 0)
    wall_score = min(max((support_strength - resistance_strength) * 5, -16), 16)
    
    velocity = delta_score + flow_micro_score + iv_score + pain_score + flow_score + wall_score
    
    if velocity >= 30:
        signal = "STRONG BULLISH"
        risk_level = "HIGH CONVICTION"
        target_shift = (velocity / 100) * 0.03
    elif velocity > 5:
        signal = "BULLISH"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.02
    elif velocity <= -30:
        signal = "STRONG BEARISH"
        risk_level = "HIGH CONVICTION"
        target_shift = (velocity / 100) * 0.03
    elif velocity < -5:
        signal = "BEARISH"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.02
    else:
        signal = "NEUTRAL (SIDEWAYS CHOP)"
        risk_level = "LOW (THETA DECAY)"
        target_shift = 0.0
        
    price_target = cp * (1 + target_shift)
    
    insights = []
    if delta_score > 15: insights.append("Strong dealer positive delta exposure detected; squeeze upward likely.")
    elif delta_score < -15: insights.append("Negative delta dominance; heavy put selling observed.")
    if abs(flow_micro_score) > 6: insights.append("Near-ATM traded flow is reinforcing the directional move.")
    if abs(pain_diff_pct) > 1.5: insights.append(f"High pin risk: Market pulled towards Max Pain at {max_pain}.")
    if flow_score > 10: insights.append("Smart Money (FIIs) have significantly positioned long.")
    if abs(wall_score) > 6: insights.append("Support-resistance wall strength is asymmetric, increasing squeeze potential.")
    
    return {
        "algorithm_name": "Titan Elite: Net-Gamma & Volatility Squeeze",
        "category": "INSTITUTIONAL MASTER",
        "signal": signal,
        "velocity_score": round(velocity, 1),
        "confidence": min(abs(int(velocity)) + 40, 99),
        "price_target_mid": round(price_target, 2),
        "price_target_low": round(price_target * 0.992, 2),
        "price_target_high": round(price_target * 1.008, 2),
        "key_insight": " | ".join(insights) if insights else "Multi-dimensional indicators show neutral positioning.",
        "risk_level": risk_level,
        "theme": "warning",  # Used for UI coloring
        "breakdown": {
            "Delta Imbalance Weight": f"{round(delta_score, 1)}%",
            "Near-ATM Flow Force": f"{round(flow_micro_score, 1)}%",
            "Volatility Skew Force": f"{round(iv_score, 1)}%",
            "Max Pain Gravity": f"{round(pain_score, 1)}%",
            "Institutional Flow Bias": f"{round(flow_score, 1)}%",
            "Wall Strength Bias": f"{round(wall_score, 1)}%"
        }
    }


def run_oi_concentration_matrix(ctx):
    """
    Alpha-Omega: Institutional Order Flow & OI Concentration Matrix
    Analyzes the 'Tug-of-War' between Call writers and Put writers, distance to walls,
    and Volume vs OI divergences.
    """
    summary = ctx.get('summary', {})
    cp = ctx.get('current_price', 0)
    if cp == 0: cp = 1 # Avoid division errors

    c_oi = summary.get('highest_call_oi', 1)
    p_oi = summary.get('highest_put_oi', 1)
    if c_oi == 0: c_oi = 1
    if p_oi == 0: p_oi = 1

    # 1. Absolute OI Ratio (Weight: 40%)
    # If Put OI >> Call OI, strong support exists. 
    oi_ratio = p_oi / c_oi
    oi_ratio_score = min(max((oi_ratio - 1) * 30, -40), 40)
    
    # 2. Distance to OI Walls (Weight: 30%)
    c_strike = summary.get('highest_call_oi_strike', cp * 1.05)
    p_strike = summary.get('highest_put_oi_strike', cp * 0.95)
    
    dist_c = abs(c_strike - cp) / cp
    dist_p = abs(cp - p_strike) / cp
    # If price is very close to Put strike, risk of breakdown or bounce.
    # If dist_p < dist_c, support is closer than resistance.
    wall_distance_score = min(max((dist_c - dist_p) * 500, -30), 30)

    # 3. PCR Divergence (Weight: 30%)
    pcr_vol = summary.get('pcr_volume', 1.0)
    pcr_oi = summary.get('pcr_oi', 1.0)
    # Divergence: If Volume PCR is very high but OI PCR is low, it means intraday buying isn't converting to overnight positional strength.
    divergence = pcr_vol - pcr_oi
    divergence_score = min(max(divergence * 40, -30), 30)
    near_pcr = float(summary.get('near_atm_pcr_volume') or pcr_vol)
    near_pressure_score = min(max((near_pcr - 1) * 35, -22), 22)
    support_strength = float(summary.get('support_strength') or 0)
    resistance_strength = float(summary.get('resistance_strength') or 0)
    wall_strength_score = min(max((support_strength - resistance_strength) * 6, -25), 25)
    
    velocity = oi_ratio_score + wall_distance_score + divergence_score + near_pressure_score + wall_strength_score
    
    if velocity >= 35:
        signal = "STRONG SUPPORT BREAKOUT"
        risk_level = "HIGH CONVICTION"
        target_shift = (velocity / 100) * 0.025
    elif velocity > 10:
        signal = "BULLISH CONTINUATION"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.015
    elif velocity <= -35:
        signal = "STRONG RESISTANCE REJECTION"
        risk_level = "HIGH CONVICTION"
        target_shift = (velocity / 100) * 0.025
    elif velocity < -10:
        signal = "BEARISH REJECTION"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.015
    else:
        signal = "RANGE BOUND COMPRESSION"
        risk_level = "LOW"
        target_shift = 0.0

    price_target = cp * (1 + target_shift)
    
    insights = []
    if oi_ratio > 1.5: insights.append(f"Massive Put writing detected at {p_strike}. Steel floor support.")
    elif oi_ratio < 0.6: insights.append(f"Call writers aggressively defending {c_strike} zone.")
    if abs(divergence) > 0.4: insights.append("Severe divergence between Intraday Volume and Positional OI.")
    if abs(wall_strength_score) > 7: insights.append("Near-ATM wall strength confirms the broader OI structure.")

    return {
        "algorithm_name": "Alpha-Omega: OI Concentration Matrix",
        "category": "INSTITUTIONAL MASTER",
        "signal": signal,
        "velocity_score": round(velocity, 1),
        "confidence": min(abs(int(velocity)) + 30, 99),
        "price_target_mid": round(price_target, 2),
        "price_target_low": p_strike if velocity < 0 else round(price_target * 0.99, 2),
        "price_target_high": c_strike if velocity > 0 else round(price_target * 1.01, 2),
        "key_insight": " | ".join(insights) if insights else "OI blocks are symmetrically balanced.",
        "risk_level": risk_level,
        "theme": "info",  # Blue theme
        "breakdown": {
            "OI Put/Call Imbalance Vector": f"{round(oi_ratio_score, 1)}%",
            "Wall Proximity Pull": f"{round(wall_distance_score, 1)}%",
            "Volume-OI Divergence Delta": f"{round(divergence_score, 1)}%",
            "Near-ATM PCR Pressure": f"{round(near_pressure_score, 1)}%",
            "Wall Strength Skew": f"{round(wall_strength_score, 1)}%",
            "Resistance Zone Distance": f"{round(dist_c*100, 1)}%"
        }
    }


def run_quantum_vega_premium(ctx):
    """
    Quantum Vega: Macro Volatility & Risk Premium Engine
    Checks idiosyncratic Vol levels against global macro (VIX/DOW) to gauge
    unseen event/earnings risk.
    """
    summary = ctx.get('summary', {})
    mkt = ctx.get('market_context', {})
    cp = ctx.get('current_price', 0)
    
    # 1. IV vs VIX Spread (Weight: 40%)
    atm_iv = summary.get('atm_iv', 15)
    india_vix = float(mkt.get('india_vix') or 15)
    # If IV is > 2x VIX, stock is pricing intense independent crisis/event. (High crush risk usually bearish for trend)
    iv_spread = atm_iv - india_vix
    premium_score = -min(max(iv_spread * 2, -40), 40) # Negative because too high premium = overbought/crush
    
    # 2. Global Macro Tailwind (Weight: 35%)
    # DOW/Nifty changes
    nifty_chg = float(mkt.get('nifty_change_points') or 0)
    dow_chg = float(mkt.get('dow_jones_change_points') or 0)
    asia_score = (
        float(mkt.get('hangseng_change_points') or 0) * 0.03
        + float(mkt.get('nikkei_change_points') or 0) * 0.02
        + float(mkt.get('shanghai_composite_change') or 0) * 12
    )
    europe_score = (
        float(mkt.get('dax_change_points') or 0) * 0.04
        + float(mkt.get('ftse_change_points') or 0) * 0.06
        + float(mkt.get('cac40_change_points') or 0) * 0.05
    )
    macro_score = min(max((nifty_chg * 0.1) + (dow_chg * 0.05) + asia_score + europe_score, -35), 35)
    
    # 3. Commodity/Currency Friction (Weight: 25%)
    dxy = float(mkt.get('dollar_index_dxy') or 104)
    # Strong dollar usually hurts emerging markets
    crude = float(mkt.get('crude_oil_price') or 85)
    usd_inr = float(mkt.get('usd_inr') or 84.2)
    dxy_score = min(max((104 - dxy) * 5 + (85 - crude) * 1.2 + (84.2 - usd_inr) * 3, -25), 25)
    
    velocity = premium_score + macro_score + dxy_score
    
    if velocity >= 30:
        signal = "BULLISH VOLATILITY EXPANSION"
        risk_level = "HIGH (BREAKOUT)"
        target_shift = (velocity / 100) * 0.02
    elif velocity > 5:
        signal = "BULLISH DRIFT"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.01
    elif velocity <= -30:
        signal = "BEARISH IV CRUSH EXPECTED"
        risk_level = "HIGH CONVICTION"
        target_shift = (velocity / 100) * 0.02
    elif velocity < -5:
        signal = "MACRO DRAG DOWN"
        risk_level = "MODERATE"
        target_shift = (velocity / 100) * 0.01
    else:
        signal = "FAIRLY PRICED VRP"
        risk_level = "LOW RISK"
        target_shift = 0.0
        
    price_target = cp * (1 + target_shift)
    
    insights = []
    if iv_spread > 15: insights.append(f"Idiosyncratic Risk High: Stock IV ({atm_iv}%) is detached from VIX ({india_vix}%). Premium collapse likely.")
    elif iv_spread < -5: insights.append("Options are anomalously cheap compared to market volatility.")
    if macro_score > 20: insights.append("Global macro tailwinds strongly supporting upward momentum.")
    elif macro_score < -20: insights.append("Heavy global macro headwinds dragging sector down.")
    if abs(dxy_score) > 8: insights.append("Dollar, crude, and FX regime are materially affecting local risk appetite.")

    return {
        "algorithm_name": "Quantum Vega: Risk Premium Engine",
        "category": "INSTITUTIONAL MASTER",
        "signal": signal,
        "velocity_score": round(velocity, 1),
        "confidence": min(abs(int(velocity)) + 35, 99),
        "price_target_mid": round(price_target, 2),
        "price_target_low": round(price_target * 0.985, 2),
        "price_target_high": round(price_target * 1.015, 2),
        "key_insight": " | ".join(insights) if insights else "Volatility Risk Premium matches global macro metrics.",
        "risk_level": risk_level,
        "theme": "danger", # Red/Pink theme
        "breakdown": {
            "IV vs VIX Spread Risk": f"{round(premium_score, 1)}%",
            "Global Macro Composite": f"{round(macro_score, 1)}%",
            "Currency Friction (DXY)": f"{round(dxy_score, 1)}%",
            "Implied Option Fairness": f"{round(100 - abs(premium_score), 1)}%"
        }
    }
