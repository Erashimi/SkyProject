from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(sample_data):
    filtered = filter_by_state(sample_data, "EXECUTED")
    assert all(item["state"] == "EXECUTED" for item in filtered)


def test_sort_by_date(sample_data):
    sorted_asc = sort_by_date(sample_data, reverse=False)
    dates = [item["date"] for item in sorted_asc]
    assert dates == ["2023-01-01", "2023-02-01", "2023-03-01"]

    sorted_desc = sort_by_date(sample_data)
    dates = [item["date"] for item in sorted_desc]
    assert dates == ["2023-03-01", "2023-02-01", "2023-01-01"]
