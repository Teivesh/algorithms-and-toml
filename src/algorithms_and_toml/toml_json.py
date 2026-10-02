"""Convert a TOML document to JSON with its arrays sorted."""
import argparse
import json
import tomllib
from datetime import date, datetime, time
from pathlib import Path
from typing import Any


def _sort_key(value: Any) -> tuple[int, Any]:
    """Comparable deterministic key for JSON scalar values."""
    if isinstance(value, bool): return (0, value)
    if isinstance(value, (int, float)): return (1, value)
    if isinstance(value, str): return (2, value)
    if isinstance(value, dict): return (3, json.dumps(value, ensure_ascii=False, sort_keys=True, default=str))
    if value is None: return (4, "")
    return (5, str(value))


def sort_arrays(value: Any) -> Any:
    """Recursively sort arrays while retaining tables and scalar values."""
    if isinstance(value, dict): return {key: sort_arrays(item) for key, item in value.items()}
    if isinstance(value, list): return sorted((sort_arrays(item) for item in value), key=_sort_key)
    if isinstance(value, (date, datetime, time)): return value.isoformat()
    return value


def convert_toml(text: str) -> dict[str, Any]:
    """Parse TOML; require three top-level fields and sort all arrays."""
    document = tomllib.loads(text)
    if len(document) < 3:
        raise ValueError("TOML document must contain at least three top-level fields")
    return sort_arrays(document)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="source TOML file")
    parser.add_argument("output", type=Path, help="destination JSON file")
    args = parser.parse_args()
    result = convert_toml(args.input.read_text(encoding="utf-8"))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
