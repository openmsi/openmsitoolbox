"Pytest fixtures and hooks shared across all test modules."

import logging
import shutil
import pytest


@pytest.fixture
def logger():
    """Provide a simple logger for tests."""
    log = logging.getLogger("pytest_test")
    log.setLevel(logging.DEBUG)
    yield log
    # cleanup if needed


@pytest.fixture
def output_dir(tmp_path, request):
    """Create and manage an output directory per test."""
    test_dir = tmp_path / request.node.name
    test_dir.mkdir()
    yield test_dir
    # Pytest auto-cleans tmp_path, but you can explicitly handle success/failure
    if request.node.rep_call.passed:
        shutil.rmtree(test_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Hook that attaches test results (setup/call/teardown) to the test item."""
    # yield to let pytest run the test and get its report
    outcome = yield
    rep = outcome.get_result()
    # attach report attributes to the test item, like item.rep_call
    setattr(item, "rep_" + rep.when, rep)
