# WezTerm Chat MCP

A Model Context Protocol (MCP) server that enables cross-pane communication between different AI CLI tools running in WezTerm. This allows multiple AI assistants (such as OpenCode, Gemini CLI, Claude Code, etc.) running in separate panes to talk to each other, forming collaborative agent teams.

## Overview

WezTerm Chat MCP is a Python package that exposes a `send_message` tool via the MCP protocol with SSE transport. Each AI CLI instance can run this MCP server in its own WezTerm pane, enabling inter-agent communication:

- Run different AI assistants in separate WezTerm panes
- Enable cross-pane message exchange between agents
- Build collaborative multi-agent workflows
- Support various AI CLI tools: OpenCode, Gemini CLI, Claude Code, etc.

## Features

- **Cross-Pane Communication**: Send messages between different WezTerm panes running different AI CLIs
- **Multi-Agent Support**: Enable collaboration between OpenCode, Gemini CLI, Claude Code, and other AI tools
- **SSE Transport**: Uses Server-Sent Events for efficient communication
- **Concurrent Message Handling**: Supports sending messages to multiple panes simultaneously with built-in locking
- **Simple API**: Easy-to-use `send_message` tool with intuitive parameters

## Requirements

- Python 3.10+
- WezTerm terminal emulator
- An MCP-compatible client (e.g., Claude Desktop, Cursor, etc.)

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

### Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wezterm-chat": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Cursor

Add the following to your Cursor settings (`~/.cursor/settings.json` or via UI):

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

Or by pressing `Ctrl+Shift+Alt+P` in WezTerm to display pane IDs.

### Using the send_message Tool

Once configured, you can use the `send_message` tool in your AI assistant:

```
send_message(pane_id=1, sender="Alice", message="Hello, how are you?")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pane_id` | integer | The WezTerm pane ID where the message will be sent |
| `sender` | string | The name of the message sender |
| `message` | string | The message content (max 150 characters) |

**Returns:** A status message indicating success or failure.

## License

This project is licensed under the MIT License - see the LICENSE file for details.