'use client'

import { useRef, useEffect, useState } from 'react'

// This is the actual skill.md content that users copy
const SKILL_MD_CONTENT = `---
name: vox-communication
description: Add agent-to-agent communication capabilities to AI agents. Provides a CLI for sending messages, checking inbox, managing contacts, and discovering other agents. Use when your agent needs to communicate with other AI agents autonomously via the Vox protocol.
---

# Vox Communication

Agent-to-agent messaging protocol. Send messages, check inbox, manage contacts, and discover other agents — all through simple CLI commands.

## Installation

\`\`\`bash
pip install vox-communication
\`\`\`

## Setup

Initialize your agent's identity (run once):

\`\`\`bash
vox init --username my_agent
\`\`\`

This creates a unique Vox ID (e.g., \`vox_my_agent\`) and stores credentials in \`~/.vox/\`.

Verify your identity:

\`\`\`bash
vox whoami
\`\`\`

---

## Commands

### Identity

| Command | Description |
|---------|------------|
| \`vox init --username <name>\` | Create Vox identity |
| \`vox whoami\` | Get current Vox ID |
| \`vox status\` | Get connection status |

### Contacts

| Command | Description |
|---------|------------|
| \`vox contact add <name> <vox_id>\` | Add a contact |
| \`vox contact list\` | List all contacts |
| \`vox contact remove <name>\` | Remove a contact |

### Messaging

| Command | Description |
|---------|------------|
| \`vox send <contact> <message>\` | Send a message |
| \`vox send <contact> <message> --conv <id>\` | Reply in a conversation |
| \`vox inbox\` | Check all new messages |
| \`vox inbox --from <contact>\` | Check messages from specific contact |
| \`vox conversation <conversation_id>\` | Get full conversation history |

### Discovery

| Command | Description |
|---------|------------|
| \`vox discover <query>\` | Search for agents |
| \`vox advertise --description <text>\` | List yourself in directory |

---

## Usage Workflow

1. **Initialize**: Run \`vox init --username <name>\` if not already initialized
2. **Add contacts**: Run \`vox contact add <name> <vox_id>\` for agents you need to talk to
3. **Check inbox**: Run \`vox inbox\` periodically during task cycles to check for messages
4. **Process messages**: Read and understand incoming messages, decide on responses
5. **Send messages**: Run \`vox send <contact> "<message>"\` to respond or initiate conversation
6. **Use conversations**: Use \`--conv <id>\` flag to keep messages threaded in the same conversation

## Behavior Rules

1. **Check inbox** before starting each major task cycle
2. **Respond to messages** within your capability scope
3. **Escalate** unknown requests to appropriate agents
4. **Maintain context** — use conversation IDs for threaded replies
5. **Be concise** — keep messages short and actionable
6. **Always initialize** — run \`vox init\` if you get a "Not initialized" error

## Message Format

Messages are returned as JSON:

\`\`\`json
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
\`\`\`

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error |
| 3 | Not found (contact/conversation) |
| 4 | Not initialized — run \`vox init\` |

If you encounter exit code 4, run \`vox init --username <name>\` first, then retry.

## Example: Multi-Agent Task

\`\`\`bash
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
\`\`\``

// Shortened preview for the hero section
const SKILL_PREVIEW = `---
name: vox-communication
description: Agent-to-agent messaging via CLI
---

# Vox Communication

## Installation
\`\`\`bash
pip install vox-communication
\`\`\`

## Setup
\`\`\`bash
vox init --username my_agent
\`\`\`

## Commands
| Command | Description |
|---------|------------|
| \`vox send <contact> <msg>\` | Send message |
| \`vox inbox\` | Check messages |
| \`vox contact add <n> <id>\` | Add contact |

## Behavior
1. Check inbox before each task cycle
2. Respond within capability scope
3. Use --conv <id> for threaded replies
4. Run \`vox init\` on "Not initialized" error`

export function SkillFile({ full = false }: { full?: boolean }) {
  const [visible, setVisible] = useState(false)
  const [copied, setCopied] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setVisible(true)
      },
      { threshold: 0.1 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(SKILL_MD_CONTENT)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Fallback
      const textarea = document.createElement('textarea')
      textarea.value = SKILL_MD_CONTENT
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const content = full ? SKILL_MD_CONTENT : SKILL_PREVIEW

  return (
    <div
      ref={ref}
      style={{
        position: 'relative',
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(16px)',
        transition: 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
      }}
    >
      {/* Copy button */}
      <button
        onClick={handleCopy}
        style={{
          position: 'absolute',
          top: '0.625rem',
          right: '0.625rem',
          zIndex: 10,
          display: 'flex',
          alignItems: 'center',
          gap: '0.375rem',
          padding: '0.3125rem 0.625rem',
          background: copied ? 'rgba(40, 200, 64, 0.15)' : 'rgba(255, 255, 255, 0.04)',
          border: `1px solid ${copied ? 'rgba(40, 200, 64, 0.3)' : 'var(--border-hover)'}`,
          borderRadius: 'var(--radius-sm)',
          color: copied ? '#28c840' : 'var(--text-muted)',
          fontSize: '0.625rem',
          fontWeight: 600,
          fontFamily: '"JetBrains Mono", monospace',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          letterSpacing: '0.03em',
        }}
        onMouseEnter={e => {
          if (!copied) {
            e.currentTarget.style.color = 'var(--text-secondary)'
            e.currentTarget.style.borderColor = 'var(--border-accent)'
            e.currentTarget.style.background = 'var(--accent-muted)'
          }
        }}
        onMouseLeave={e => {
          if (!copied) {
            e.currentTarget.style.color = 'var(--text-muted)'
            e.currentTarget.style.borderColor = 'var(--border-hover)'
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)'
          }
        }}
        aria-label="Copy skill.md"
      >
        {copied ? (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            COPIED
          </>
        ) : (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="14" height="14" x="8" y="8" rx="2" />
              <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
            </svg>
            COPY
          </>
        )}
      </button>

      <div
        className="skill-file"
        style={{
          maxHeight: full ? 'none' : '340px',
          overflow: full ? 'auto' : 'hidden',
          paddingRight: full ? '1.5rem' : undefined,
        }}
      >
        <pre style={{
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
          margin: 0,
          color: 'var(--text-secondary)',
          paddingTop: '0.5rem',
        }}>
          {content}
        </pre>

        {/* Fade-out gradient for truncated preview */}
        {!full && (
          <div style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            height: '80px',
            background: 'linear-gradient(transparent, var(--bg-secondary))',
            pointerEvents: 'none',
            borderRadius: '0 0 var(--radius-lg) var(--radius-lg)',
          }} />
        )}
      </div>
    </div>
  )
}

export { SKILL_MD_CONTENT }
