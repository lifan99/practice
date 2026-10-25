"""Keep environment validation separate from unfinished practice checks."""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-exercises",
        action="store_true",
        default=False,
        help="Run exercise checks, including unfinished TODO functions.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-exercises"):
        return
    skip = pytest.mark.skip(reason="Use --run-exercises to enable practice checks.")
    for item in items:
        if item.get_closest_marker("exercise"):
            item.add_marker(skip)
