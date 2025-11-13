import asyncio
import pytest
from openmsitoolbox import ControlledProcessAsync

TIMEOUT_SECS = 10


class ControlledProcessAsyncForTesting(ControlledProcessAsync):
    """
    Minimal example to use for testing ControlledProcessAsync
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.checked = False
        self.on_shutdown_called = False
        self.post_run_called = False

    async def run_task(self):
        while self.alive:
            if self.counter < 5:
                self.counter += 1
            await asyncio.sleep(1)

    def _on_check(self):
        self.checked = True

    def _on_shutdown(self):
        self.on_shutdown_called = True

    async def _post_run(self):
        self.post_run_called = True


@pytest.mark.asyncio
async def test_controlled_process_async():
    """Test the async ControlledProcessAsync behavior."""
    cpa = ControlledProcessAsyncForTesting(update_secs=5)
    assert cpa.counter == 0

    stop_event = asyncio.Event()

    async def assertions():
        await asyncio.sleep(1)
        await cpa.control_command_queue.put("c")
        await cpa.control_command_queue.put("check")
        await asyncio.sleep(1)
        assert cpa.checked
        assert not cpa.on_shutdown_called
        assert not cpa.post_run_called

        await cpa.control_command_queue.put("q")
        await asyncio.sleep(2.0)
        assert cpa.on_shutdown_called
        assert cpa.post_run_called
        stop_event.set()

    # Run the process loop + assertions concurrently
    await asyncio.wait_for(
        asyncio.gather(cpa.run_loop(), assertions(), stop_event.wait()),
        timeout=TIMEOUT_SECS,
    )
