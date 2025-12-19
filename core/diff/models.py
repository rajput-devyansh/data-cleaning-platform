from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RowDiff:
    row_id: int
    changes: Dict[str, Dict[str, object]]
    # example:
    # {
    #   "CSAT_Score": {"before": 3, "after": 5},
    #   "Priority": {"before": "low", "after": "high"}
    # }


@dataclass
class DiffSummary:
    rows_added: int
    rows_removed: int
    rows_modified: int


@dataclass
class DatasetDiff:
    summary: DiffSummary
    added_row_ids: List[int]
    removed_row_ids: List[int]
    modified_rows: List[RowDiff]