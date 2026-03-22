from __future__ import annotations


def score_event_confidence(
    model_confidence: float,
    *,
    geocoding_confidence: float | None,
    date_precision: str,
) -> float:
    date_score = {
        "day": 1.0,
        "season": 0.8,
        "year": 0.7,
        "range": 0.65,
        "century-range": 0.5,
        "unknown": 0.35,
    }.get(date_precision, 0.35)

    geo_score = geocoding_confidence if geocoding_confidence is not None else 0.25
    score = 0.55 * model_confidence + 0.25 * geo_score + 0.20 * date_score
    return round(max(0.0, min(1.0, score)), 2)
