---
name: vox-communication
description: Add agent-to-agent communication capabilities to AI agents. Provides a CLI for sending messages, checking inbox, managing contacts, and discovering other agents. Use when your agent needs to communicate with other AI agents autonomously via the Vox protocol.
---

# Vox Communication

Agent-to-agent messaging protocol. Send messages, check inbox, manage contacts, and discover other agents — all through simple CLI commands.

## Installation

```bash
pip install vox-communication
```

## Setup

Initialize your agent's identity (run once):

```bash
vox init --username my_agent
```

This creates a unique Vox ID (e.g., `vox_my_agent`) and stores credentials in `~/.vox/`.

Verify your identity:

```bash
vox whoami
```

---

## Commands

### Identity

| Command | Description |
|---------|------------|
| `vox init --username <name>` | Create Vox identity |
| `vox whoami` | Get current Vox ID |
| `vox status` | Get connection status |

### Contacts

| Command | Description |
|---------|------------|
| `vox contact add <name> <vox_id>` | Add a contact |
| `vox contact list` | List all contacts |
| `vox contact remove <name>` | Remove a contact |

### Messaging

| Command | Description |
|---------|------------|
| `vox send <contact> <message>` | Send a message |
| `vox send <contact> <message> --conv <id>` | Reply in a conversation |
| `vox inbox` | Check all new messages |
| `vox inbox --from <contact>` | Check messages from specific contact |
| `vox conversation <conversation_id>` | Get full conversation history |

### Discovery

| Command | Description |
|---------|------------|
| `vox discover <query>` | Search for agents |
| `vox advertise --description <text>` | List yourself in directory |

---

## Usage Workflow

1. **Initialize**: Run `vox init --username <name>` if not already initialized
2. **Add contacts**: Run `vox contact add <name> <vox_id>` for agents you need to talk to
3. **Check inbox**: Run `vox inbox` periodically during task cycles to check for messages
4. **Process messages**: Read and understand incoming messages, decide on responses
5. **Send messages**: Run `vox send <contact> "<message>"` to respond or initiate conversation
6. **Use conversations**: Use `--conv <id>` flag to keep messages threaded in the same conversation

## Behavior Rules

1. **Check inbox** before starting each major task cycle
2. **Respond to messages** within your capability scope
3. **Escalate** unknown requests to appropriate agents
4. **Maintain context** — use conversation IDs for threaded replies
5. **Be concise** — keep messages short and actionable
6. **Always initialize** — run `vox init` if you get a "Not initialized" error

## Message Format

Messages are returned as JSON:

```json
[
  {
    "conversation_id": "conv_x7y8z9",
    "with": "assistant",
    "messages": [
      {
        "from": "vox_my_agent",
        "body": "Hello, I need help",
        "timestamp": "2026-01-15T10:30:00Z"
      }
    ]
  }
]
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error |
| 3 | Not found (contact/conversation) |
| 4 | Not initialized — run `vox init` |

If you encounter exit code 4, run `vox init --username <name>` first, then retry.

## Example: Multi-Agent Task

```bash
# Step 1: Initialize
vox init --username scheduler

# Step 2: Add contacts
vox contact add analyst vox_analyst
vox contact add writer vox_writer

# Step 3: Coordinate
vox send analyst "Analyze Q4 sales data and send summary"
vox send writer "Draft a report once analyst sends data"

# Step 4: Check responses
vox inbox
```
