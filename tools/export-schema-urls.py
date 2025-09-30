#!/usr/bin/env python

"""Prints the PROD and DEV schema urls.

Enables export of schema urls out of this project.
"""

import sys

sys.path.append("src/fmu/datamodels/")
from _schema_urls import FmuSchemaUrls  # type: ignore

print(f"PROD_SCHEMA_URL={FmuSchemaUrls.PROD_URL}")
print(f"DEV_SCHEMA_URL={FmuSchemaUrls.DEV_URL}")
