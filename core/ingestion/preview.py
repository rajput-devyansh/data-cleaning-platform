import pandas as pd
from pathlib import Path

def load_preview(
    file_path: Path,
    encoding: str,
    delimiter: str,
    has_header: bool,
    nrows: int = 20,
):
    return pd.read_csv(
        file_path,
        encoding=encoding,
        sep=delimiter,
        header=0 if has_header else None,
        nrows=nrows,
    )