"Tests for single-threaded and multi-threaded ControlledProcess variants."

import time
import pytest
from openmsitoolbox.utilities.exception_tracking_thread import ExceptionTrackingThread
from openmsitoolbox import ControlledProcessSingleThread, ControlledProcessMultiThreaded

TIMEOUT_SECS = 10
N_THREADS = 3


class ControlledProcessSingleThreadForTesting(ControlledProcessSingleThread):
    """Single-threaded ControlledProcess subclass for testing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.checked = False
        self.on_shutdown_called = False

    def _on_check(self):
        self.checked = True

    def _on_shutdown(self):
        self.on_shutdown_called = True

    def _run_iteration(self):
        if self.counter < 5:
            self.counter += 1


class ControlledProcessMultiThreadedForTesting(ControlledProcessMultiThreaded):
    """Multi-threaded ControlledProcess subclass for testing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.checked = False
        self.on_shutdown_called = False

    def _on_check(self):
        self.checked = True

    def _on_shutdown(self):
        super()._on_shutdown()
        self.on_shutdown_called = True

    def _run_worker(self):
        while self.alive:
            if self.counter < 5:
                with self.lock:
                    self.counter += 1


@pytest.mark.parametrize(
    "process_class,kwargs",
    [
        (ControlledProcessSingleThreadForTesting, {"update_secs": 5}),
        (
            ControlledProcessMultiThreadedForTesting,
            {"n_threads": N_THREADS, "update_secs": 5},
        ),
    ],
)
def test_controlled_process(process_class, kwargs):
    """Test both single- and multi-threaded controlled process variants."""
    cp = process_class(**kwargs)
    assert cp.counter == 0

    run_thread = ExceptionTrackingThread(target=cp.run)
    run_thread.start()

    try:
        # --- pre-check ---
        assert not cp.checked

        # --- trigger commands ---
        time.sleep(1.0)
        cp.control_command_queue.put("c")
        cp.control_command_queue.put("check")
        time.sleep(1.0)

        # --- assertions ---
        assert cp.checked
        assert not cp.on_shutdown_called

        # --- shutdown ---
        cp.control_command_queue.put("q")
        time.sleep(2.0)

        assert cp.on_shutdown_called
        run_thread.join(timeout=TIMEOUT_SECS)

        if run_thread.is_alive():
            pytest.fail(f"Thread timed out after {TIMEOUT_SECS}s")

        assert cp.counter == 5

    finally:
        if run_thread.is_alive():
            cp.shutdown()
            run_thread.join(timeout=5)
            if run_thread.is_alive():
                pytest.fail("Thread did not terminate after forced shutdown")
