import datetime

from django.conf import settings

from dashboard.algorithms.core import derive_market_features, safe_float
from dashboard.models import (
    AlgoPerformanceMetrics,
    SuperBrainMemory,
    SuperBrainPredictionRecord,
    AlgoPredictionRecord,
)


def _algo_weight(metric):
    if not metric:
        return 1.0
    return max(0.6, min(1.8, (metric.combined_score / 100.0) + (metric.rolling_10_accuracy / 200.0)))


def _signal_to_signed(signal):
    if 'BULLISH' in signal:
        return 1
    if 'BEARISH' in signal:
        return -1
    return 0


def _build_reasoning(stock_symbol, signal, confidence, top_algos, key_factors, disagreement_pct, features):
    top_algo_names = ", ".join(item['algo'] for item in top_algos[:3]) or "historical core models"
    factor_text = ", ".join(f"{item['factor']} ({item['impact']})" for item in key_factors[:3])
    macro_tone = "supportive" if features['global_macro_bias'] >= 0 else "fragile"
    option_tone = "constructive" if (features['near_atm_pressure_bias'] + features['support_strength_bias']) >= 0 else "defensive"
    return (
        f"{stock_symbol} ke liye Super Brain ka net bias {signal} hai with {round(confidence, 1)}% confidence. "
        f"Highest trusted alignment {top_algo_names} se mila, jabki main deciding drivers {factor_text} rahe. "
        f"Global backdrop {macro_tone} hai aur option microstructure {option_tone} dikha raha hai. "
        f"Model disagreement {round(disagreement_pct, 1)}% hai, isliye setup ko opening confirmation ke saath trade karna better hoga."
    )


def _scenario_payload(signal_strength, current_price, expected_move):
    bull_target = round(current_price * (1 + expected_move * (1.1 + max(signal_strength, 0) / 160) / 100), 2)
    base_target = round(current_price * (1 + signal_strength / 220 / 100), 2)
    bear_target = round(current_price * (1 - expected_move * (1.1 + max(-signal_strength, 0) / 160) / 100), 2)
    return {
        "bull_case": {
            "condition": "Opening above resistance zone with sustained call unwinding and positive global carry.",
            "price_target": bull_target,
            "probability_pct": 30 if signal_strength < 0 else 45,
        },
        "base_case": {
            "condition": "Price respects option walls and trades inside expected move range.",
            "price_target": base_target,
            "probability_pct": 35,
        },
        "bear_case": {
            "condition": "Support breakdown plus weak global setup and seller follow-through.",
            "price_target": bear_target,
            "probability_pct": 35 if signal_strength < 0 else 20,
        },
    }


def run_super_brain(stock_symbol, date, option_chain_summary, market_context, algo_results, historical_features=None):
    metrics = {m.algo_name: m for m in AlgoPerformanceMetrics.objects.filter(stock_symbol=stock_symbol)}
    features = derive_market_features({
        'summary': option_chain_summary,
        'market_context': market_context,
        'historical_features': historical_features or {},
        'current_price': option_chain_summary.get('underlying_price', 0),
    })
    current_price = safe_float(option_chain_summary.get('underlying_price') or option_chain_summary.get('atm_strike'))

    weighted_votes = []
    for algo in algo_results:
        metric = metrics.get(algo['algorithm_name'])
        weight = _algo_weight(metric) * max(0.55, min(1.4, safe_float(algo.get('confidence'), 50) / 100))
        weighted_votes.append({
            'algo': algo['algorithm_name'],
            'signal': algo['signal'],
            'signed_vote': _signal_to_signed(algo['signal']),
            'weight': round(weight, 3),
            'confidence': algo.get('confidence', 50),
        })

    total_weight = sum(abs(item['weight']) for item in weighted_votes) or 1.0
    net_vote = sum(item['signed_vote'] * item['weight'] for item in weighted_votes)
    disagreement_pct = 100 - (abs(net_vote) / total_weight * 100)
    feature_vote = (
        features['delta_bias'] * 0.12
        + features['near_atm_pressure_bias'] * 0.16
        + features['support_strength_bias'] * 0.10
        + features['wall_balance'] * 0.08
        + features['global_macro_bias'] * 0.16
        + features['flow_balance_bias'] * 0.10
        + features['currency_oil_bias'] * 0.06
        + features['volatility_risk_bias'] * 0.06
        + features['max_pain_bias'] * 0.06
        + features['vol_regime'] * 0.04
        + features['downside_hedging_bias'] * 0.06
    )
    final_score = max(-100.0, min(100.0, net_vote * 24 + feature_vote * 0.62))

    if final_score >= 18:
        signal = "BULLISH"
    elif final_score <= -18:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"

    expected_move = features['expected_move_pct']
    target_shift_pct = (final_score / 100.0) * expected_move
    price_target = current_price * (1 + target_shift_pct / 100.0)
    price_range_low = price_target - (current_price * expected_move / 100.0)
    price_range_high = price_target + (current_price * expected_move / 100.0)
    confidence = max(40.0, min(93.0, 48 + abs(final_score) * 0.32 + (100 - disagreement_pct) * 0.18))

    top_algos = sorted(weighted_votes, key=lambda item: abs(item['signed_vote'] * item['weight']), reverse=True)[:5]
    ranked_factor_pool = [
        ("Near-ATM flow pressure", features['near_atm_pressure_bias']),
        ("Global macro alignment", features['global_macro_bias']),
        ("Support vs resistance strength", features['support_strength_bias']),
        ("Delta positioning", features['delta_bias']),
        ("Option wall balance", features['wall_balance']),
        ("Downside hedging premium", features['downside_hedging_bias']),
        ("Flow balance FII/DII", features['flow_balance_bias']),
        ("Volatility regime", features['vol_regime']),
        ("Currency and crude pressure", features['currency_oil_bias']),
        ("Max pain gravity", features['max_pain_bias']),
    ]
    key_factors = []
    for rank, (label, value) in enumerate(sorted(ranked_factor_pool, key=lambda item: abs(item[1]), reverse=True)[:5], start=1):
        impact = "NEUTRAL" if abs(value) < 8 else ("BULLISH" if value > 0 else "BEARISH")
        key_factors.append({"rank": rank, "factor": label, "impact": impact, "score": round(value, 2)})
    scenarios = _scenario_payload(final_score, current_price, expected_move)
    reasoning = _build_reasoning(stock_symbol, signal, confidence, top_algos, key_factors, disagreement_pct, features)

    try:
        memory = SuperBrainMemory.objects.get(stock_symbol=stock_symbol)
        memory_text = memory.accumulated_learnings
    except SuperBrainMemory.DoesNotExist:
        memory_text = ""

    prediction_data = {
        "signal": signal,
        "confidence": round(confidence, 2),
        "price_target": round(price_target, 2),
        "price_range_low": round(price_range_low, 2),
        "price_range_high": round(price_range_high, 2),
        "reasoning_hinglish": reasoning,
        "key_factors": key_factors,
        "algo_disagreement_analysis": (
            f"Weighted disagreement {round(disagreement_pct, 1)}% hai. "
            f"Top supporting models: {', '.join(item['algo'] for item in top_algos[:3])}."
        ),
        "scenarios": scenarios,
        "overall_market_prediction": signal,
        "risk_warning": (
            "Yeh report evidence-based hai lekin certainty nahi. "
            "Opening gap, news flow, global macro reversal, aur liquidity change scenario ko invalidate kar sakte hain."
        ),
        "self_learning_note": memory_text[-300:] if memory_text else "Fresh memory cycle.",
        "coordination_snapshot": {
            "net_vote": round(net_vote, 3),
            "disagreement_pct": round(disagreement_pct, 2),
            "top_algos": top_algos,
            "feature_vote": round(feature_vote, 2),
            "global_macro_bias": round(features['global_macro_bias'], 2),
            "near_atm_pressure_bias": round(features['near_atm_pressure_bias'], 2),
        },
    }

    record, _ = SuperBrainPredictionRecord.objects.update_or_create(
        date=date,
        stock_symbol=stock_symbol,
        defaults=dict(
            total_algos_consulted=len(algo_results),
            input_market_context=market_context,
            input_algo_results=algo_results,
            historical_performance_context={
                'algo_weights': {name: round(_algo_weight(metric), 3) for name, metric in metrics.items()},
                'coordination_snapshot': prediction_data['coordination_snapshot'],
            },
            super_brain_signal=prediction_data['signal'],
            super_brain_price_low=prediction_data['price_range_low'],
            super_brain_price_high=prediction_data['price_range_high'],
            super_brain_price_target=prediction_data['price_target'],
            super_brain_confidence=prediction_data['confidence'],
            super_brain_reasoning=prediction_data['reasoning_hinglish'],
            super_brain_key_factors=prediction_data['key_factors'],
            bull_case=scenarios['bull_case'],
            base_case=scenarios['base_case'],
            bear_case=scenarios['bear_case'],
        )
    )
    return prediction_data, record


def teach_super_brain(stock_symbol, date, actual_close):
    prediction = SuperBrainPredictionRecord.objects.get(stock_symbol=stock_symbol, date=date)
    prev_target = safe_float(prediction.super_brain_price_target)
    actual_signal = "BULLISH" if actual_close >= prev_target else "BEARISH"
    was_correct = (
        (prediction.super_brain_signal == "BULLISH" and actual_signal == "BULLISH")
        or (prediction.super_brain_signal == "BEARISH" and actual_signal == "BEARISH")
        or (prediction.super_brain_signal == "NEUTRAL" and abs(actual_close - prev_target) / actual_close < 0.007)
    )
    price_error_pct = abs(actual_close - prev_target) / actual_close * 100 if actual_close else 0
    accuracy_score = max(0, 100 - price_error_pct * (1.4 if was_correct else 2.1))

    algo_insights = []
    for record in AlgoPredictionRecord.objects.filter(stock_symbol=stock_symbol, date=date):
        algo_insights.append(f"{record.algo_name}: {'sahi' if record.direction_correct else 'galat'}")

    post_analysis = (
        f"Actual close ₹{round(actual_close, 2)} raha. Super Brain signal {prediction.super_brain_signal} tha "
        f"aur target ₹{round(prev_target, 2)} tha. {'Direction hold hui.' if was_correct else 'Direction miss hui.'}"
    )
    prediction.actual_close = actual_close
    prediction.was_correct = was_correct
    prediction.accuracy_score = round(accuracy_score, 2)
    prediction.post_analysis_hinglish = post_analysis
    prediction.save()

    update_super_brain_memory(
        stock_symbol=stock_symbol,
        new_learning=f"{post_analysis} Price error {round(price_error_pct, 2)}%.",
        new_pattern=f"Signal={prediction.super_brain_signal}, Actual={actual_signal}",
        algo_insights=" | ".join(algo_insights[:6]),
        was_correct=was_correct,
        accuracy_score=round(accuracy_score, 2),
    )
    return {
        "post_analysis": post_analysis,
        "accuracy_score": round(accuracy_score, 2),
        "was_correct": was_correct,
    }


def update_super_brain_memory(stock_symbol, new_learning, new_pattern, algo_insights, was_correct, accuracy_score):
    memory, _ = SuperBrainMemory.objects.get_or_create(
        stock_symbol=stock_symbol,
        defaults={
            'accumulated_learnings': '',
            'pattern_library': {},
            'algo_trust_weights': {},
            'market_context_patterns': {},
            'accuracy_history': [],
        }
    )

    today = str(datetime.date.today())
    history = list(memory.accuracy_history)
    history.append({'date': today, 'accuracy': accuracy_score, 'correct': was_correct})

    pattern_library = dict(memory.pattern_library)
    pattern_library[today] = new_pattern
    pattern_library = dict(list(pattern_library.items())[-25:])

    updated_learnings = (
        memory.accumulated_learnings
        + f"\n[{today}] {new_learning} Pattern: {new_pattern}. Algo snapshot: {algo_insights}."
    )
    if len(updated_learnings) > settings.MEMORY_COMPRESS_THRESHOLD:
        updated_learnings = updated_learnings[-settings.MEMORY_COMPRESS_THRESHOLD:]

    memory.accumulated_learnings = updated_learnings
    memory.pattern_library = pattern_library
    memory.accuracy_history = history[-30:]
    memory.total_days_learned = len(memory.accuracy_history)
    memory.save()
