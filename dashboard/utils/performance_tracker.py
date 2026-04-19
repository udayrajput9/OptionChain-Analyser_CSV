from dashboard.models import AlgoPredictionRecord, AlgoPerformanceMetrics
from collections import defaultdict

def update_algo_performance_metrics(stock_symbol):
    all_records = AlgoPredictionRecord.objects.filter(
        stock_symbol=stock_symbol,
        direction_correct__isnull=False
    ).order_by('date')
    
    algo_data = defaultdict(list)
    for r in all_records:
        algo_data[r.algo_name].append({
            'correct': r.direction_correct,
            'price_hit': r.price_in_range,
            'confidence': r.confidence_score,
            'date': r.date
        })
        
    for algo_name, records in algo_data.items():
        total = len(records)
        if total == 0: continue
        
        correct_dir = sum(1 for r in records if r['correct'])
        price_hits = sum(1 for r in records if r['price_hit'])
        
        recent = records[-10:]
        rolling_acc = sum(1 for r in recent if r['correct']) / len(recent) * 100 if recent else 50.0
        
        avg_confidence = sum(r['confidence'] for r in records) / total
        actual_accuracy = (correct_dir / total) * 100
        calibration = actual_accuracy / avg_confidence if avg_confidence > 0 else 1.0
        
        combined = (correct_dir / total * 70) + (price_hits / total * 30)
        
        AlgoPerformanceMetrics.objects.update_or_create(
            stock_symbol=stock_symbol,
            algo_name=algo_name,
            defaults={
                'total_predictions': total,
                'correct_direction': correct_dir,
                'price_range_hits': price_hits,
                'direction_accuracy': round(actual_accuracy, 2),
                'price_accuracy': round(price_hits / total * 100, 2),
                'combined_score': round(combined, 2),
                'rolling_10_accuracy': round(rolling_acc, 2),
                'confidence_calibration_score': round(calibration, 3)
            }
        )
