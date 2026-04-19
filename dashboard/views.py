import datetime
from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.utils import timezone

from .algorithms.core import safe_float
from .algorithms.master_hf_algo import (
    run_institutional_squeeze_model,
    run_oi_concentration_matrix,
    run_quantum_vega_premium,
)
from .algorithms.prediction_engine import compile_all_algorithm_results
from .algorithms.super_brain import run_super_brain, teach_super_brain
from .forms import MarketContextForm, OptionChainUploadForm
from .models import (
    AlgoPerformanceMetrics,
    AlgoPredictionRecord,
    MarketContext,
    SuperBrainMemory,
    SuperBrainPredictionRecord,
)
from .utils.data_cleaner import get_option_chain_summary, parse_option_chain_csv
from .utils.data_loader import (
    delete_stock_card_files,
    get_available_files,
    get_available_stocks,
    get_file_by_number,
    load_historical_data_until,
    parse_date_label,
    reset_stock_files,
    save_uploaded_option_chain,
)
from .utils.performance_tracker import update_algo_performance_metrics
from .utils.report_builder import build_professional_report


SLOT_ORDER = {
    MarketContext.SLOT_0910: 1,
    MarketContext.SLOT_1300: 2,
    MarketContext.SLOT_1500: 3,
}


def sort_contexts_desc(contexts):
    return sorted(contexts, key=lambda ctx: (ctx.date, SLOT_ORDER.get(ctx.context_slot, 0)), reverse=True)


def serialize_market_context(context_obj):
    """Convert MarketContext object to JSON-serializable dict, handling Decimal fields"""
    if not context_obj:
        return {}
    
    serialized = {}
    for key, value in context_obj.__dict__.items():
        if key.startswith('_'):
            continue
        
        # Handle Decimal fields - convert to float
        if isinstance(value, Decimal):
            serialized[key] = float(value)
        # Handle date objects - convert to ISO string
        elif isinstance(value, datetime.date):
            serialized[key] = value.isoformat()
        # Handle other types as-is
        else:
            serialized[key] = value
    
    return serialized


def get_slot_status_map(stock_symbol, target_date):
    filled_slots = set(
        MarketContext.objects.filter(stock_symbol=stock_symbol, date=target_date).values_list('context_slot', flat=True)
    )
    return {
        slot_value: slot_value in filled_slots
        for slot_value, _ in MarketContext.SLOT_CHOICES
    }


def clear_stock_database_records(stock_symbol):
    deleted_counts = {
        'market_contexts': MarketContext.objects.filter(stock_symbol=stock_symbol).delete()[0],
        'algo_predictions': AlgoPredictionRecord.objects.filter(stock_symbol=stock_symbol).delete()[0],
        'algo_metrics': AlgoPerformanceMetrics.objects.filter(stock_symbol=stock_symbol).delete()[0],
        'super_brain_predictions': SuperBrainPredictionRecord.objects.filter(stock_symbol=stock_symbol).delete()[0],
        'super_brain_memory': SuperBrainMemory.objects.filter(stock_symbol=stock_symbol).delete()[0],
    }
    return deleted_counts


def enrich_algo_card_data(algo_output, current_stock_price):
    try:
        low = float(algo_output.get('price_target_low', current_stock_price * 0.99))
        high = float(algo_output.get('price_target_high', current_stock_price * 1.01))
    except Exception:
        low, high = current_stock_price * 0.99, current_stock_price * 1.01

    mid = (low + high) / 2
    range_width = high - low
    range_pct = (range_width / current_stock_price) * 100 if current_stock_price else 0
    pos_pct = min(100, max(0, (current_stock_price - low) / range_width * 100)) if range_width > 0 else 50
    icons = {
        'Random Forest Options Analyzer': 'RF',
        'XGBoost IV Surface Predictor': 'XG',
        'LSTM Temporal Pattern Detector': 'LS',
        'Transformer Attention Model': 'TR',
        'Prophet Time Series Forecaster': 'PR',
        'Monte Carlo Simulation Engine': 'MC',
        'GARCH Volatility Forecaster': 'GV',
        'LightGBM Options Mispricing Detector': 'LG',
        'SVM Regime Classifier': 'SV',
        'Ensemble Meta-Learner': 'EN',
        'Black-Scholes Greeks Analysis': 'BS',
        'Max Pain Theory': 'MP',
        'PCR Contrarian Analysis': 'PC',
        'OI Concentration Analysis': 'OI',
        'IV Skew Analysis': 'IV',
        'Gamma Exposure GEX Analysis': 'GX',
        'Unusual Options Activity Detector': 'UA',
        'Delta Hedging Flow Predictor': 'DH',
        'IV Term Structure Analysis': 'TS',
        'Theoretical Value Arbitrage Scanner': 'AR',
    }
    algo_output.update({
        'price_target_mid': round(mid, 2),
        'range_width': round(range_width, 2),
        'range_pct': round(range_pct, 2),
        'current_price_pct_in_range': round(pos_pct, 1),
        'icon': icons.get(algo_output.get('algorithm_name'), 'AI'),
    })
    return algo_output


def compute_historical_features(stock_symbol, upto_number):
    snapshots = []
    for item in load_historical_data_until(stock_symbol, upto_number, last_n=6):
        summary = get_option_chain_summary(item['data'], item['meta'])
        snapshots.append({'summary': summary, 'meta': item['meta'], 'file_info': item['file_info']})
    if len(snapshots) <= 1:
        return {'history_count': len(snapshots), 'price_trend_pct': 0.0, 'iv_trend_pct': 0.0, 'delta_trend': 0.0}

    from .algorithms.core import summarize_history

    return summarize_history(snapshots)


def build_intraday_comparison(stock_symbol, current_file_number, current_summary):
    previous_files = [file_info for file_info in get_available_files(stock_symbol) if file_info['number'] < current_file_number]
    if not previous_files:
        return None

    previous_file = previous_files[-1]
    prev_df, prev_meta = parse_option_chain_csv(previous_file['path'])
    previous_summary = get_option_chain_summary(prev_df, prev_meta)

    keys = [
        ('underlying_price', 'Underlying Price'),
        ('atm_iv', 'ATM IV'),
        ('pcr_volume', 'Volume PCR'),
        ('near_atm_pcr_volume', 'Near-ATM PCR'),
        ('near_atm_delta_flow', 'Near-ATM Delta Flow'),
        ('liquidity_score', 'Liquidity Score'),
        ('max_pain', 'Max Pain'),
        ('highest_call_oi_strike', 'Call Wall'),
        ('highest_put_oi_strike', 'Put Wall'),
        ('net_delta', 'Net Delta'),
        ('iv_skew', 'IV Skew'),
        ('downside_iv_premium', 'Downside IV Premium'),
    ]
    comparisons = []
    for key, label in keys:
        current_value = float(current_summary.get(key, 0) or 0)
        previous_value = float(previous_summary.get(key, 0) or 0)
        change = current_value - previous_value
        comparisons.append({
            'label': label,
            'current': round(current_value, 2),
            'previous': round(previous_value, 2),
            'change': round(change, 2),
        })

    return {
        'previous_file': previous_file,
        'previous_summary': previous_summary,
        'rows': comparisons,
    }


def resolve_analysis_date(stock_symbol, file_info):
    parsed_file_date = parse_date_label(file_info.get('date_label'))
    if parsed_file_date:
        return parsed_file_date

    context = MarketContext.objects.filter(stock_symbol=stock_symbol).order_by('-date').first()
    if context:
        return context.date
    return datetime.date.today()


def resolve_market_context(stock_symbol, analysis_date):
    stock_symbol = stock_symbol.upper()
    exact_contexts = list(MarketContext.objects.filter(stock_symbol=stock_symbol, date=analysis_date))
    if exact_contexts:
        return sort_contexts_desc(exact_contexts)[0]
    prior_contexts = list(MarketContext.objects.filter(stock_symbol=stock_symbol, date__lte=analysis_date))
    if prior_contexts:
        return sort_contexts_desc(prior_contexts)[0]
    any_contexts = list(MarketContext.objects.filter(stock_symbol=stock_symbol))
    return sort_contexts_desc(any_contexts)[0] if any_contexts else None


def get_algo_results_with_outcomes(stock_symbol, date):
    predictions = AlgoPredictionRecord.objects.filter(stock_symbol=stock_symbol, date=date)
    metrics_map = {m.algo_name: m for m in AlgoPerformanceMetrics.objects.filter(stock_symbol=stock_symbol)}
    algo_cards = []
    for pred in predictions:
        outcome_data = None
        if pred.actual_close_price is not None:
            direction_score = 70 if pred.direction_correct else 0
            price_score = 30 if pred.price_in_range else max(0, 30 - (pred.price_error_pct or 0) * 2)
            outcome_data = {
                'actual_close': pred.actual_close_price,
                'direction_correct': pred.direction_correct,
                'price_in_range': pred.price_in_range,
                'price_error_pct': pred.price_error_pct,
                'score': round(direction_score + price_score, 2),
            }
        card_data = enrich_algo_card_data(pred.full_algo_output, float(pred.predicted_price_target))
        card_data.update({'outcome': outcome_data, 'metrics': metrics_map.get(pred.algo_name)})
        algo_cards.append(card_data)
    algo_cards.sort(key=lambda card: card.get('metrics').combined_score if card.get('metrics') else 0, reverse=True)
    return algo_cards


def get_algo_summary(algo_cards):
    total = len(algo_cards)
    bullish = sum(1 for card in algo_cards if 'BULLISH' in card['signal'])
    bearish = sum(1 for card in algo_cards if 'BEARISH' in card['signal'])
    neutral = total - bullish - bearish
    correct = sum(1 for card in algo_cards if card['outcome'] and card['outcome']['direction_correct'])
    wrong = sum(1 for card in algo_cards if card['outcome'] and not card['outcome']['direction_correct'])
    pending = sum(1 for card in algo_cards if not card['outcome'])
    acc = round(correct / (correct + wrong) * 100, 1) if (correct + wrong) else None
    return {
        'total': total,
        'prediction': {'bullish': bullish, 'bearish': bearish, 'neutral': neutral},
        'validation': {'correct': correct, 'wrong': wrong, 'pending': pending},
        'accuracy_today': acc,
    }


def build_coordination_snapshot(algo_cards):
    bullish = [card for card in algo_cards if 'BULLISH' in card['signal']]
    bearish = [card for card in algo_cards if 'BEARISH' in card['signal']]
    dominant = bullish if len(bullish) >= len(bearish) else bearish
    agreement_score = (len(dominant) / len(algo_cards) * 100) if algo_cards else 0
    return {
        'agreement_score': agreement_score,
        'top_aligned_algos': [card['algorithm_name'] for card in dominant[:5]],
        'is_coordinated': agreement_score >= 55,
    }


class DashboardView(View):
    def get(self, request):
        stocks = get_available_stocks()
        today = timezone.localdate()
        stock_data = {}
        for symbol in stocks:
            files = get_available_files(symbol)
            stock_contexts = list(MarketContext.objects.filter(stock_symbol=symbol))
            latest_context = sort_contexts_desc(stock_contexts)[0] if stock_contexts else None
            stock_data[symbol] = {
                'file_count': len(files),
                'latest_file': files[-1] if files else None,
                'no_files': len(files) == 0,
                'latest_context_date': latest_context.date if latest_context else None,
                'latest_context_slot': latest_context.get_context_slot_display() if latest_context else None,
                'slot_statuses': get_slot_status_map(symbol, today),
            }
        return render(request, 'dashboard/index.html', {'stocks': stocks, 'stock_data': stock_data, 'today': today})


class UploadView(View):
    def get(self, request):
        initial_stock = (request.GET.get('stock') or '').strip().upper()
        initial_slot = request.GET.get('slot') or MarketContext.SLOT_1500
        initial_date = request.GET.get('date') or timezone.localdate()
        return render(request, 'dashboard/upload.html', {
            'form': MarketContextForm(initial={'stock_symbol': initial_stock, 'context_slot': initial_slot, 'date': initial_date}),
            'upload_form': OptionChainUploadForm(initial={'stock_symbol': initial_stock}),
        })

    def post(self, request):
        if 'csv_file' in request.FILES:
            upload_form = OptionChainUploadForm(request.POST, request.FILES)
            form = MarketContextForm()
            if upload_form.is_valid():
                file_info = save_uploaded_option_chain(
                    upload_form.cleaned_data['stock_symbol'],
                    upload_form.cleaned_data['csv_file'],
                )
                return redirect('report', stock=upload_form.cleaned_data['stock_symbol'], date=file_info['number'])
            return render(request, 'dashboard/upload.html', {'form': form, 'upload_form': upload_form})

        form = MarketContextForm(request.POST)
        upload_form = OptionChainUploadForm()
        if form.is_valid():
            cleaned = form.cleaned_data
            ctx, _ = MarketContext.objects.update_or_create(
                date=cleaned['date'],
                stock_symbol=cleaned['stock_symbol'],
                context_slot=cleaned['context_slot'],
                defaults=cleaned,
            )
            AlgoPredictionRecord.objects.filter(stock_symbol=ctx.stock_symbol, date=ctx.date).delete()
            SuperBrainPredictionRecord.objects.filter(stock_symbol=ctx.stock_symbol, date=ctx.date).delete()
            messages.success(request, f"{ctx.stock_symbol} ka {ctx.get_context_slot_display()} form save ho gaya.")
            latest_file = get_available_files(ctx.stock_symbol)
            if latest_file:
                return redirect('report', stock=ctx.stock_symbol, date=latest_file[-1]['number'])
            return redirect('index')
        return render(request, 'dashboard/upload.html', {'form': form, 'upload_form': upload_form})


class StockResetView(View):
    def post(self, request, stock):
        stock = stock.upper()
        removed_files = reset_stock_files(stock)
        clear_stock_database_records(stock)
        messages.warning(
            request,
            f"{stock} reset ho gaya. {removed_files} CSV files aur saara trained/prediction/form data clear kar diya gaya."
        )
        return redirect('index')


class StockDeleteView(View):
    def post(self, request, stock):
        stock = stock.upper()
        clear_stock_database_records(stock)
        deleted_folder = delete_stock_card_files(stock)
        if deleted_folder:
            messages.error(request, f"{stock} card aur uska saara data delete kar diya gaya.")
        else:
            messages.error(request, f"{stock} ka folder nahi mila, lekin related database data clear kar diya gaya.")
        return redirect('index')


class ReportView(View):
    def get(self, request, stock, date):
        file_info = get_file_by_number(stock, date)
        df, meta = parse_option_chain_csv(file_info['path'])
        summary_stats = get_option_chain_summary(df, meta)
        analysis_date = resolve_analysis_date(stock, file_info)
        context_obj = resolve_market_context(stock, analysis_date)
        market_context = serialize_market_context(context_obj)

        historical_features = compute_historical_features(stock, date)
        engine_ctx = {
            'stock': stock,
            'current_price': meta.get('underlying_price', 0),
            'summary': summary_stats,
            'total_days_available': len(get_available_files(stock)),
            'market_context': market_context,
            'historical_features': historical_features,
        }

        existing_predictions = AlgoPredictionRecord.objects.filter(stock_symbol=stock, date=analysis_date)
        should_refresh = (
            not existing_predictions.exists()
            or existing_predictions.exclude(file_number=date).exists()
        )
        if should_refresh:
            results = compile_all_algorithm_results(engine_ctx)
            for res in results:
                # Convert any Decimal values to float for JSON serialization
                res_serialized = {}
                for key, value in res.items():
                    if isinstance(value, Decimal):
                        res_serialized[key] = float(value)
                    else:
                        res_serialized[key] = value
                
                target = res_serialized.get('price_target_mid', (res_serialized['price_target_low'] + res_serialized['price_target_high']) / 2)
                AlgoPredictionRecord.objects.update_or_create(
                    date=analysis_date,
                    stock_symbol=stock,
                    algo_name=res_serialized['algorithm_name'],
                    defaults={
                        'file_number': date,
                        'algo_category': res_serialized['category'],
                        'predicted_signal': res_serialized['signal'],
                        'predicted_price_low': res_serialized['price_target_low'],
                        'predicted_price_high': res_serialized['price_target_high'],
                        'predicted_price_target': target,
                        'confidence_score': res_serialized['confidence'],
                        'full_algo_output': res_serialized,
                    }
                )
            run_super_brain(stock, analysis_date, summary_stats, market_context, results, historical_features)

        algo_cards = get_algo_results_with_outcomes(stock, analysis_date)
        summary = get_algo_summary(algo_cards)
        coordination = build_coordination_snapshot(algo_cards)
        sb_record = SuperBrainPredictionRecord.objects.filter(stock_symbol=stock, date=analysis_date).first()
        intraday_comparison = build_intraday_comparison(stock, date, summary_stats)
        master_algo_cards = [
            run_institutional_squeeze_model(engine_ctx),
            run_oi_concentration_matrix(engine_ctx),
            run_quantum_vega_premium(engine_ctx),
        ]
        narrative_report = build_professional_report(stock, summary_stats, market_context, algo_cards, sb_record, coordination)

        return render(request, 'dashboard/report.html', {
            'stock': stock,
            'date': file_info['date_label'],
            'analysis_date': analysis_date,
            'active_context_slot': context_obj.get_context_slot_display() if context_obj else None,
            'file': file_info,
            'all_files': get_available_files(stock),
            'meta': meta,
            'summary_stats': summary_stats,
            'algo_cards': algo_cards,
            'summary': summary,
            'master_algo_cards': master_algo_cards,
            'market_context': market_context,
            'coordination': coordination,
            'super_brain_record': sb_record,
            'intraday_comparison': intraday_comparison,
            'narrative_report': narrative_report,
            'option_chain_data': df.to_dict('records')[max(0, len(df) // 2 - 5):len(df) // 2 + 5],
        })


class PredictionView(View):
    def get(self, request, stock, date):
        file_info = get_file_by_number(stock, date)
        analysis_date = resolve_analysis_date(stock, file_info)
        sb_record = SuperBrainPredictionRecord.objects.filter(stock_symbol=stock, date=analysis_date).first()
        context_obj = resolve_market_context(stock, analysis_date)
        memory = SuperBrainMemory.objects.filter(stock_symbol=stock).first()
        metrics = AlgoPerformanceMetrics.objects.filter(stock_symbol=stock).order_by('-combined_score')
        return render(request, 'dashboard/prediction.html', {
            'stock': stock,
            'date_val': date,
            'analysis_date': analysis_date,
            'active_context_slot': context_obj.get_context_slot_display() if context_obj else None,
            'sb': sb_record,
            'memory': memory,
            'metrics': metrics,
        })


class OutcomeFeedView(View):
    def _resolve_date(self, stock, date):
        if date == 'today':
            latest = SuperBrainPredictionRecord.objects.filter(stock_symbol=stock).order_by('-date').first()
            return latest.date if latest else datetime.date.today()
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return datetime.date.today()

    def get(self, request, stock, date):
        dt = self._resolve_date(stock, date)
        predictions = AlgoPredictionRecord.objects.filter(stock_symbol=stock, date=dt, actual_close_price__isnull=True)
        super_pred = SuperBrainPredictionRecord.objects.filter(stock_symbol=stock, date=dt).first()
        return render(request, "dashboard/outcome_feed.html", {
            'predictions': predictions,
            'super_prediction': super_pred,
            'stock': stock,
            'date': dt.strftime('%Y-%m-%d'),
        })

    def post(self, request, stock, date):
        dt = self._resolve_date(stock, date)
        actual_close = float(request.POST.get('actual_close'))
        prev_close = float(request.POST.get('prev_close'))
        actual_signal = "BULLISH" if actual_close >= prev_close else "BEARISH"

        for pred in AlgoPredictionRecord.objects.filter(stock_symbol=stock, date=dt):
            was_corr = (
                ("BULLISH" in pred.predicted_signal and actual_signal == "BULLISH")
                or ("BEARISH" in pred.predicted_signal and actual_signal == "BEARISH")
                or ("NEUTRAL" in pred.predicted_signal and abs(actual_close - prev_close) / prev_close < 0.007)
            )
            in_range = float(pred.predicted_price_low) <= actual_close <= float(pred.predicted_price_high)
            err_pct = abs(actual_close - float(pred.predicted_price_target)) / actual_close * 100 if actual_close else 0
            pred.actual_close_price = actual_close
            pred.actual_signal = actual_signal
            pred.direction_correct = was_corr
            pred.price_in_range = in_range
            pred.price_error_pct = err_pct
            pred.outcome_fed_at = datetime.datetime.now()
            pred.save()

        update_algo_performance_metrics(stock)
        teach_super_brain(stock, dt, actual_close)
        return redirect('learning_report', stock=stock, date=dt.strftime('%Y-%m-%d'))


class LearningReportView(View):
    def get(self, request, stock, date):
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            dt = datetime.date.today()

        sb = SuperBrainPredictionRecord.objects.filter(stock_symbol=stock, date=dt).first()
        algos = AlgoPredictionRecord.objects.filter(stock_symbol=stock, date=dt)
        memory = SuperBrainMemory.objects.filter(stock_symbol=stock).first()
        correct_algos = algos.filter(direction_correct=True)
        wrong_algos = algos.filter(Q(direction_correct=False) | Q(direction_correct__isnull=True))
        return render(request, 'dashboard/learning_report.html', {
            'stock': stock,
            'date': date,
            'sb': sb,
            'correct_algos': correct_algos,
            'wrong_algos': wrong_algos,
            'memory': memory,
        })
