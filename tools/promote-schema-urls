#!/usr/bin/env python

"""Replaces all dev schema URLs with the prod URLs.

Should be run from the project root.
"""

import sys
from pathlib import Path

from fmu.datamodels._schema_base import FmuSchemas


def replace_schema_url(file_path: Path) -> None:
    """Replaces the dev url with the prod url in a file."""
    with file_path.open(encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(FmuSchemas.DEV_URL, FmuSchemas.PROD_URL)

    with file_path.open("w", encoding="utf-8") as f:
        f.write(new_content)


def run_replacement_on_schemas() -> None:
    """Recursively iterate through all schemas."""
    for json_file in FmuSchemas.PATH.rglob("*.json"):
        try:
            replace_schema_url(json_file)
            print(f"Processed file: {json_file}")
        except Exception as e:
            sys.exit(f"Error processing file {json_file}: {e}")


if __name__ == "__main__":
    run_replacement_on_schemas()
