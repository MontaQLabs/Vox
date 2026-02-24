'use client'

import { useState, useEffect, useRef } from 'react'

interface TerminalProps {
  title?: string
  commands: string[]
  className?: string
}

export function Terminal({ title = "vox@agent", commands, className }: TerminalProps) {
  const [displayedLines, setDisplayedLines] = useState<string[]>([])
  const [currentText, setCurrentText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isTyping, setIsTyping] = useState(true)
  const contentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (currentIndex >= commands.length) {
      setIsTyping(false)
      return
    }

    const command = commands[currentIndex]
    let charIdx = 0

    const typeInterval = setInterval(() => {
      if (charIdx <= command.length) {
        setCurrentText(command.substring(0, charIdx))
        charIdx++
      } else {
        clearInterval(typeInterval)
        setTimeout(() => {
          setDisplayedLines(prev => [...prev, command])
          setCurrentText('')
          setCurrentIndex(prev => prev + 1)
        }, 800)
      }
    }, 35)

    return () => clearInterval(typeInterval)
  }, [currentIndex, commands])

  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight
    }
  }, [displayedLines, currentText])

  return (
    <div className={`terminal ${className || ''}`}>
      <div className="terminal-header">
        <div className="terminal-dot" />
        <div className="terminal-dot" />
        <div className="terminal-dot" />
        <span className="terminal-title">{title}</span>
      </div>
      <div className="terminal-content" ref={contentRef}>
        {displayedLines.map((cmd, idx) => (
          <div key={idx} style={{ marginBottom: '0.375rem' }}>
            <span className="terminal-prompt">❯ </span>
            <span style={{ color: 'var(--text-primary)' }}>{cmd}</span>
          </div>
        ))}
        {isTyping && (
          <div style={{ marginBottom: '0.375rem' }}>
            <span className="terminal-prompt">❯ </span>
            <span style={{ color: 'var(--text-primary)' }}>{currentText}</span>
            <span className="terminal-cursor" />
          </div>
        )}
        {!isTyping && (
          <div style={{ marginBottom: '0.375rem' }}>
            <span className="terminal-prompt">❯ </span>
            <span className="terminal-cursor" />
          </div>
        )}
      </div>
    </div>
  )
}
