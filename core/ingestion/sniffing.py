import csv
from pathlib import Path
import chardet

def detect_encoding(file_path: Path, sample_size: int = 10000) -> str:
    raw = file_path.read_bytes()[:sample_size]
    result = chardet.detect(raw)
    return result["encoding"] or "utf-8"

def detect_delimiter(file_path: Path, encoding: str) -> str:
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        sample = f.read(4096)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter

def detect_header(file_path: Path, encoding: str, delimiter: str) -> bool:
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        sample = f.read(4096)
        sniffer = csv.Sniffer()
        return sniffer.has_header(sample)