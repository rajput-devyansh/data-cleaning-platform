import json
from core.diff.models import DatasetDiff


def diff_to_json(diff: DatasetDiff) -> str:
    payload = {
        "summary": diff.summary.__dict__,
        "added_row_ids": diff.added_row_ids,
        "removed_row_ids": diff.removed_row_ids,
        "modified_rows": [
            {
                "row_id": r.row_id,
                "changes": r.changes,
            }
            for r in diff.modified_rows
        ],
    }
    return json.dumps(payload, indent=2, default=str)

import csv
import io
from core.diff.models import DatasetDiff


def diff_to_csv(diff: DatasetDiff) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Header
    writer.writerow(["_row_id", "column", "before", "after"])

    for row in diff.modified_rows:
        for col, change in row.changes.items():
            writer.writerow([
                row.row_id,
                col,
                change.get("before"),
                change.get("after"),
            ])

    return buffer.getvalue()