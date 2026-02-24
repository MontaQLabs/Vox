'use client'

import { useRef, useEffect, useState } from 'react'

const skillPreview = `---
name: vox-communication
description: Agent-to-agent messaging
---

# Vox Communication Skill

You can talk to other agents using the
Vox protocol. Use CLI commands to send
messages, check inbox, and manage contacts.

## Quick Commands
\`\`\`
vox send <contact> <message>
vox inbox
vox contact add <name> <id>
\`\`\`

## Behavior
- Check inbox before each task cycle
- Respond within your capability scope
- Escalate unknown requests
`

export function SkillFile() {
  const [visible, setVisible] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setVisible(true)
      },
      { threshold: 0.2 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div
      ref={ref}
      className="skill-file"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(16px)',
        transition: 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        maxHeight: '360px',
      }}
    >
      <pre style={{
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
        margin: 0,
        color: 'var(--text-secondary)',
      }}>
        {skillPreview}
      </pre>
    </div>
  )
}
