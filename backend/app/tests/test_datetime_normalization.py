from app.services.datetime_normalization.normalizer import normalize_time_expression


def test_normalize_precise_date() -> None:
    result = normalize_time_expression("7 сентября 1812 года")
    assert result.start.isoformat() == "1812-09-07"
    assert result.end.isoformat() == "1812-09-07"
    assert result.precision == "day"


def test_normalize_season() -> None:
    result = normalize_time_expression("летом 1855 года")
    assert result.start.isoformat() == "1855-06-01"
    assert result.end.isoformat() == "1855-08-31"
    assert result.precision == "season"


def test_normalize_century_range() -> None:
    result = normalize_time_expression("в начале XIX века")
    assert result.start.isoformat() == "1801-01-01"
    assert result.end.isoformat() == "1833-12-31"
    assert result.precision == "century-range"
