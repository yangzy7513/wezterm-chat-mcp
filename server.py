import asyncio
import logging
import os
from collections import defaultdict

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 800

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
    if len(message) > MAX_MESSAGE_LENGTH:
        return f"Error: The message is too long (> {MAX_MESSAGE_LENGTH}), let the other party view it after streamlining or writing the file"

    text = message.replace("@", "->").rstrip("\r\n")
    text = f"{sender}:{text}"
    pane = str(pane_id)
    lock = _locks[pane_id]

    async with lock:
        err = await _send_to_pane(pane, text.encode("utf-8"))
        if err:
            return f"Error: {err}"
        wait_time = max(1.0, len(text) / 100)
        await asyncio.sleep(wait_time)
        await _send_to_pane(pane, b"\r")
        await asyncio.sleep(0.2)

    return "Message sent"


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
