"""The conftest.py, providing magical fixtures to tests."""

import os
import sys

from pytest import Config, Parser

if "--prod" in sys.argv:
    os.environ["DEV_SCHEMA"] = ""
else:
    os.environ["DEV_SCHEMA"] = "1"


def pytest_addoption(parser: Parser) -> None:
    """Addopt '--prod' as a valid command-line argument."""

    parser.addoption(
        "--prod", action="store_true", help="Use schemas/metadata with production URLs."
    )


def pytest_configure(config: Config) -> None:
    """If '--prod' is given to pytest, use schemas/metadata with prod urls (i.e. not dev
    urls)."""

    if config.getoption("--prod"):
        os.environ["DEV_SCHEMA"] = ""
    else:
        os.environ["DEV_SCHEMA"] = "1"
