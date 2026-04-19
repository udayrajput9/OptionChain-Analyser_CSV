from dashboard.algorithms.core import safe_float


def build_professional_report(stock, summary_stats, market_context, algo_cards, super_brain_record, coordination):
    current_price = safe_float(summary_stats.get('underlying_price') or summary_stats.get('atm_strike'))
    support = safe_float(summary_stats.get('highest_put_oi_strike'), current_price)
    resistance = safe_float(summary_stats.get('highest_call_oi_strike'), current_price)
    max_pain = safe_float(summary_stats.get('max_pain'), current_price)
    bullish = sum(1 for card in algo_cards if 'BULLISH' in card['signal'])
    bearish = sum(1 for card in algo_cards if 'BEARISH' in card['signal'])
    super_signal = getattr(super_brain_record, 'super_brain_signal', 'NEUTRAL')
    super_target = safe_float(getattr(super_brain_record, 'super_brain_price_target', current_price))
    confidence = safe_float(getattr(super_brain_record, 'super_brain_confidence', 50))
    context_slot = market_context.get('context_slot', 'CLOSE_1500')
    slot_label = {
        'MORNING_0910': '09:10 AM Global Pulse',
        'MIDDAY_1300': '01:00 PM Midday Check',
        'CLOSE_1500': '03:00 PM Closing Setup',
    }.get(context_slot, context_slot)
    gift_nifty = safe_float(market_context.get('gift_nifty_next_day_indication'))
    nifty_close = safe_float(market_context.get('nifty_close'))
    overnight_bias = "positive" if gift_nifty > nifty_close else "negative" if gift_nifty < nifty_close else "flat"
    near_atm_pcr = safe_float(summary_stats.get('near_atm_pcr_volume'), summary_stats.get('pcr_volume'))
    support_strength = safe_float(summary_stats.get('support_strength'))
    resistance_strength = safe_float(summary_stats.get('resistance_strength'))
    delta_flow = safe_float(summary_stats.get('near_atm_delta_flow'))
    asia_mix = safe_float(market_context.get('hangseng_change_points')) + safe_float(market_context.get('nikkei_change_points'))
    europe_mix = (
        safe_float(market_context.get('dax_change_points'))
        + safe_float(market_context.get('ftse_change_points'))
        + safe_float(market_context.get('cac40_change_points'))
    )
    crude = safe_float(market_context.get('crude_oil_price'))
    dxy = safe_float(market_context.get('dollar_index_dxy'))

    if super_signal == "BULLISH":
        base_strategy = f"Buy-on-dips near ₹{support:.2f} with confirmation above opening VWAP."
    elif super_signal == "BEARISH":
        base_strategy = f"Sell-on-rise below ₹{resistance:.2f} and avoid longs until support stabilises."
    else:
        base_strategy = f"Range trade between ₹{support:.2f} and ₹{resistance:.2f}; aggressive directional trades avoid karo."

    trigger_up = max(resistance, current_price)
    trigger_down = min(support, current_price)
    return {
        'headline': f"{stock} next-session outlook {super_signal} with {confidence:.1f}% model confidence. Active strategic slot: {slot_label}.",
        'executive_summary': (
            f"20 algorithms mein {bullish} bullish aur {bearish} bearish signals aaye. "
            f"Super Brain ne inhe weighted performance ke saath combine karke {super_signal} bias nikala. "
            f"Primary target ₹{super_target:.2f} hai, while max pain ₹{max_pain:.2f} near-term gravity level bana hua hai."
        ),
        'market_structure': (
            f"Current option structure mein support ₹{support:.2f} aur resistance ₹{resistance:.2f} ke around defined hai. "
            f"Overnight setup {overnight_bias} hai, India VIX {market_context.get('india_vix', 'N/A')} aur FII flow "
            f"{market_context.get('fii_data_net', 'N/A')} context ko reinforce ya challenge kar sakta hai. "
            f"Near-ATM PCR {near_atm_pcr:.2f}, delta flow {delta_flow:.3f}, aur wall strength ratio "
            f"{support_strength:.2f}/{resistance_strength:.2f} se short-term pressure samajh aata hai."
        ),
        'global_context': (
            f"US sentiment {market_context.get('us_market_sentiment', 'N/A')} hai, Asia basket {asia_mix:.2f} points composite par "
            f"aur Europe basket {europe_mix:.2f} points composite par hai. Crude {crude:.2f} aur DXY {dxy:.2f} "
            f"India risk appetite ko overnight influence kar sakte hain."
        ),
        'strategy': (
            f"{base_strategy} Entry tabhi lena jab price action opening 15-30 minute mein signal confirm kare. "
            f"False breakout avoid karne ke liye volume expansion aur option wall shift dono dekho."
        ),
        'tomorrow_map': (
            f"Agar price ₹{trigger_up:.2f} ke upar sustain kare to upside path ₹{getattr(super_brain_record, 'super_brain_price_high', super_target):.2f} ki taraf open ho sakta hai. "
            f"Agar ₹{trigger_down:.2f} toot jaye to downside pressure ₹{getattr(super_brain_record, 'super_brain_price_low', super_target):.2f} tak stretch ho sakta hai."
        ),
        'risk_controls': (
            "Trade size ko conviction ke hisaab se scale karo, binary all-in avoid karo. "
            "Gap openings, stock-specific news, earnings, aur broad index reversal is report ko invalidate kar sakte hain."
        ),
        'coordination_note': (
            f"Algorithm coordination score {coordination.get('agreement_score', 0):.1f} hai. "
            f"Top aligned models: {', '.join(coordination.get('top_aligned_algos', [])[:3]) or 'n/a'}."
        ),
    }
