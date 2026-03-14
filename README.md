# WezTerm Chat MCP

A Model Context Protocol (MCP) server that enables cross-pane communication between different AI CLI tools running in WezTerm. This allows AI assistants (such as OpenCode, Gemini CLI, Claude Code, etc.) running in separate WezTerm panes to send commands and messages to each other, forming collaborative agent teams.

## Overview

WezTerm Chat MCP is a Python package that exposes a `send_message` tool via the MCP protocol with SSE transport. It leverages WezTerm's CLI `send-text` command to enable inter-agent communication between different AI CLI instances running in separate WezTerm panes:

- Run different AI assistants in separate WezTerm panes
- Use WezTerm CLI's `send-text` command to send commands and messages between panes
- Enable cross-pane command and message exchange between agents
- Build collaborative multi-agent workflows where agents can coordinate tasks

## Features

- **Cross-Pane Communication**: Send messages between different WezTerm panes running different AI CLIs
- **Multi-Agent Support**: Enable collaboration between OpenCode, Gemini CLI, Claude Code, and other AI tools
- **SSE Transport**: Uses Server-Sent Events for efficient communication
- **Concurrent Message Handling**: Supports sending messages to multiple panes simultaneously with built-in locking
- **Simple API**: Easy-to-use `send_message` tool with intuitive parameters

## Requirements

- Python 3.10+
- [WezTerm terminal emulator](https://wezterm.org/index.html)
- [opencode](https://opencode.ai/) (recommend)

## Installation

### From Source

```bash
git clone https://github.com/yangzy7513/wezterm-chat-mcp.git
cd wezterm-chat-mcp
pip install -e .
```

## Configuration

This MCP server uses SSE (Server-Sent Events) transport and must run inside WezTerm for stable interaction. This ensures the server can reliably communicate with WezTerm's CLI for sending messages to panes.

### Starting the Server in WezTerm

Start the MCP server in a WezTerm window or tab:

```bash
wezterm-chat
```

The server will listen on `http://localhost:8000` via SSE.

### OpenCode

Add the following to your OpenCode configuration file:

```json
{
  "mcpServers": {
    "wezterm-chat": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Claude Code

Add the following to your Claude Code configuration file:

```json
{
  "mcpServers": {
    "wezterm-chat": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Other MCP Clients

Configure your MCP client to connect to `http://localhost:8000/sse`.

## Usage

### Getting the Pane ID

Before sending messages, you need to identify the WezTerm pane ID. You can get it using:

```bash
wezterm cli list-panes --format json
```

This will display all panes with their IDs in JSON format.

### Using the send_message Tool

Once configured, you can use the `send_message` tool in your AI assistant:

```
send_message(pane_id=1, sender="Alice", message="Hello, how are you?")
```

**Message Format:**
- Messages are sent in the format: `{sender}:{message}`
- Maximum message length: 800 characters

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pane_id` | integer | The WezTerm pane ID where the message will be sent |
| `sender` | string | The name of the message sender |
| `message` | string | The message content (max 800 characters) |

**Returns:** A status message indicating success or failure.