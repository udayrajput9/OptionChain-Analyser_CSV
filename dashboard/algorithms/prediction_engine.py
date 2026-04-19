from .ml_algorithms import ALL_ML_ALGORITHMS
from .hedgefund_algorithms import ALL_HF_ALGORITHMS
from .core import derive_market_features, safe_float

def compile_all_algorithm_results(ctx):
    ctx = dict(ctx)
    ctx['derived_features'] = derive_market_features(ctx)
    results = []
    
    for algo_func in ALL_ML_ALGORITHMS:
        res = algo_func(ctx)
        # Add basic info
        res['current_price'] = ctx['current_price']
        results.append(res)
        
    for algo_func in ALL_HF_ALGORITHMS:
        res = algo_func(ctx)
        res['current_price'] = ctx['current_price']
        results.append(res)
        
    return results

def calculate_global_market_score(market_context):
    score = 0
    reasoning = []
    
    if market_context:
        gn = float(market_context.get('gift_nifty_next_day_indication') or 0)
        nifty_close = float(market_context.get('nifty_close') or 0)
        if gn and nifty_close:
            if gn > nifty_close + 50:
                score += 3
                reasoning.append("Gift Nifty strongly positive (+50 pts)")
            elif gn > nifty_close:
                score += 1
                reasoning.append("Gift Nifty mildly positive")
            elif gn < nifty_close - 50:
                score -= 3
                reasoning.append("Gift Nifty strongly negative (-50 pts)")
            else:
                score -= 1
                reasoning.append("Gift Nifty mildly negative")
                
        # Simplified US
        if market_context.get('us_market_sentiment') == 'STRONG_BULLISH':
            score += 2
            reasoning.append("US sentiment strongly bullish")
        elif market_context.get('us_market_sentiment') == 'BULLISH':
            score += 1
            reasoning.append("US sentiment supportive")
        elif market_context.get('us_market_sentiment') == 'BEARISH':
            score -= 1
            reasoning.append("US sentiment weak")
        elif market_context.get('us_market_sentiment') == 'STRONG_BEARISH':
            score -= 2
            reasoning.append("US sentiment strongly bearish")

        asia = (
            safe_float(market_context.get('hangseng_change_points')) / 120
            + safe_float(market_context.get('nikkei_change_points')) / 180
            + safe_float(market_context.get('shanghai_composite_change')) * 2
        )
        if asia > 2:
            score += 2
            reasoning.append("Asia composite positive")
        elif asia < -2:
            score -= 2
            reasoning.append("Asia composite weak")

        europe = (
            safe_float(market_context.get('dax_change_points')) / 90
            + safe_float(market_context.get('ftse_change_points')) / 45
            + safe_float(market_context.get('cac40_change_points')) / 70
        )
        if europe > 2:
            score += 1
            reasoning.append("Europe markets adding tailwind")
        elif europe < -2:
            score -= 1
            reasoning.append("Europe markets under pressure")
            
        fii = float(market_context.get('fii_data_net') or 0)
        if fii > 1000:
            score += 2
            reasoning.append("Strong FII buying")
        elif fii < -1000:
            score -= 2
            reasoning.append("Heavy FII selling")

        dxy = safe_float(market_context.get('dollar_index_dxy'))
        if dxy:
            if dxy < 102:
                score += 1
                reasoning.append("Dollar softness supports EM risk")
            elif dxy > 105:
                score -= 1
                reasoning.append("Dollar strength may pressure risk assets")

        crude = safe_float(market_context.get('crude_oil_price'))
        if crude:
            if crude < 80:
                score += 1
                reasoning.append("Lower crude supports India macros")
            elif crude > 90:
                score -= 1
                reasoning.append("High crude is a macro drag")
            
    if score >= 4:
        return "STRONGLY BULLISH — Market strong upar jayega", score, reasoning
    elif score >= 1:
        return "BULLISH — Market positive opening expected", score, reasoning
    elif score >= -1:
        return "NEUTRAL — Choppy / sideways movement expected", score, reasoning
    elif score >= -3:
        return "BEARISH — Market negative, caution rakho", score, reasoning
    else:
        return "STRONGLY BEARISH — Significant selling pressure expected", score, reasoning

def generate_tomorrow_prediction(option_data_summary, market_context, all_algo_results):
    bullish_count = sum(1 for a in all_algo_results if 'BULLISH' in a['signal'])
    bearish_count = sum(1 for a in all_algo_results if 'BEARISH' in a['signal'])
    
    if bullish_count > bearish_count + 5:
        consensus_signal = "BULLISH"
    elif bearish_count > bullish_count + 5:
        consensus_signal = "BEARISH"
    else:
        consensus_signal = "NEUTRAL"
        
    market_pred, score, reasons = calculate_global_market_score(market_context)
    
    current_price = safe_float(option_data_summary.get('underlying_price') or option_data_summary.get('atm_strike'))
    expected_move = max(0.8, min(4.0, safe_float(option_data_summary.get('atm_iv'), 18.0) / 12))
    return {
        "consensus_signal": consensus_signal,
        "consensus_confidence": min(100, max(50, abs(bullish_count - bearish_count) * 5 + 50)),
        "price_range_tomorrow": {
            "low": round(current_price * (1 - expected_move / 100), 2),
            "high": round(current_price * (1 + expected_move / 100), 2),
            "most_likely": round(current_price, 2)
        },
        "scenarios": {
            "bull_case": "If GIFT Nifty remains positive and FII buying continues.",
            "base_case": "If market opens flat, reliance on option walls.",
            "bear_case": "If global sentiment shifts overnight."
        },
        "key_levels": {
            "support": option_data_summary.get('highest_put_oi_strike', 0),
            "resistance": option_data_summary.get('highest_call_oi_strike', 0),
            "max_pain": option_data_summary.get('max_pain', 0)
        },
        "overall_market_prediction": market_pred,
        "global_reasons": reasons,
        "algo_agreement_count": max(bullish_count, bearish_count),
        "final_verdict_hinglish": f"Kal ke liye market {consensus_signal} dikh raha hai based on {max(bullish_count, bearish_count)}/20 algorithms agreeing."
    }
