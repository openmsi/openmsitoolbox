"Pytest fixtures and hooks shared across all test modules."

import shutil
import pytest


@pytest.fixture
def output_dir(tmp_path, request):
    """Provide an isolated output directory per test, kept on failure for debugging."""
    test_dir = tmp_path / request.node.name
    test_dir.mkdir()
    yield test_dir
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.passed:
        shutil.rmtree(test_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Hook that attaches test results (setup/call/teardown) to the test item."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
