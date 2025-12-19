def build_dataset_timeline(actions):
    """
    Returns a list of rows suitable for a table:
    version/order, step, rows_before, rows_after, rows_quarantined
    """
    timeline = []

    for idx, action in enumerate(actions, start=1):
        p = action["parameters"]

        timeline.append(
            {
                "order": idx,
                "step": action["step"],
                "operation": action["operation"],
                "rows_before": p.get("rows_before"),
                "rows_after": p.get("rows_after"),
                "rows_quarantined": p.get("rows_quarantined"),
                "timestamp": action["created_at"],
            }
        )

    return timeline

def build_row_count_series(actions):
    series = []

    for action in actions:
        p = action["parameters"]
        if "rows_after" in p:
            series.append(
                {
                    "timestamp": action["created_at"],
                    "rows": p.get("rows_after"),
                }
            )

    return series

def build_action_impact(actions):
    impact = []

    for action in actions:
        p = action["parameters"]
        if "rows_changed" in p:
            impact.append(
                {
                    "operation": action["operation"],
                    "rows_changed": abs(p.get("rows_changed", 0)),
                }
            )

    return impact

def build_column_overwrite_summary(actions):
    summary = {}

    for action in actions:
        p = action["parameters"]
        col = p.get("column")
        if col and "column_stats_before" in p:
            summary.setdefault(col, 0)
            summary[col] += 1

    return [
        {"column": col, "overwrite_count": cnt}
        for col, cnt in summary.items()
    ]