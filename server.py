import asyncio
import logging
import os
from collections import defaultdict

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 150

_ENV = os.environ.copy()
_locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

mcp = FastMCP("WezTerm Send")


async def _send_to_pane(pane: str, data: bytes, timeout: float = 10.0) -> str | None:
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            "wezterm",
            "cli",
            "send-text",
            "--pane-id",
            pane,
            "--no-paste",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=_ENV,
        )

        _, stderr = await asyncio.wait_for(
            proc.communicate(input=data), timeout=timeout
        )

        if proc.returncode == 0:
            return None

        return f"wezterm exit {proc.returncode}: {stderr.decode('utf-8', errors='ignore').strip()}"

    except asyncio.TimeoutError:
        if proc is not None and proc.returncode is None:
            try:
                proc.kill()
                await asyncio.wait_for(proc.wait(), timeout=2.0)
            except (OSError, asyncio.TimeoutError):
                pass
        return "WezTerm IPC timeout"

    except OSError as e:
        return f"Process spawn error: {e}"


@mcp.tool()
async def send_message(pane_id: int, sender: str, message: str) -> str:
    """Send a message to a digital employee for communication.

    Args:
        pane_id: The WezTerm pane ID where the target digital employee is located.
        sender: The name of the sender.
        message: The message content.
    """
    if not message or not sender:
        return "Error: sender and message must not be empty."
    if len(message) > MAX_MESSAGE_LENGTH:
        return f"Error: message too long (max {MAX_MESSAGE_LENGTH} chars)."

    text = f"{sender}:{message}"
    pane = str(pane_id)
    lock = _locks[pane_id]

    async with lock:
        err = await _send_to_pane(pane, text.encode("utf-8"), timeout=10.0)
        if err:
            return f"Error sending text: {err}"

        await asyncio.sleep(0.15)

        err = await _send_to_pane(pane, b"\r", timeout=3.0)
        if err:
            return f"Error sending Enter: {err}"

    return "Message sent."


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
