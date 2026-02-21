'use client'

import { useState, useEffect } from 'react'

interface TerminalProps {
  title?: string
  commands: string[]
  className?: string
}

export function Terminal({ title = "vox@agent", commands, className }: TerminalProps) {
  const [currentCommand, setCurrentCommand] = useState(0)
  const [currentText, setCurrentText] = useState('')
  const [isTyping, setIsTyping] = useState(true)

  useEffect(() => {
    if (currentCommand >= commands.length) {
      setIsTyping(false)
      return
    }

    const command = commands[currentCommand]
    let charIndex = 0

    const typeInterval = setInterval(() => {
      if (charIndex <= command.length) {
        setCurrentText(command.substring(0, charIndex))
        charIndex++
      } else {
        clearInterval(typeInterval)
        setTimeout(() => {
          setCurrentCommand(currentCommand + 1)
          setCurrentText('')
        }, 1000)
      }
    }, 50)

    return () => clearInterval(typeInterval)
  }, [currentCommand, commands])

  return (
    <div className={`terminal ${className}`}>
      <div className="terminal-header">
        <div className="terminal-dot bg-red-500"></div>
        <div className="terminal-dot bg-yellow-500"></div>
        <div className="terminal-dot bg-green-500"></div>
        <span className="ml-4 text-sm font-mono">{title}</span>
      </div>
      <div className="terminal-content">
        {commands.slice(0, currentCommand).map((cmd, idx) => (
          <div key={idx} className="mb-2">
            <span className="text-muted-foreground">$</span> {cmd}
          </div>
        ))}
        {isTyping && (
          <div className="mb-2">
            <span className="text-muted-foreground">$</span> {currentText}
            <span className="animate-pulse">_</span>
          </div>
        )}
      </div>
    </div>
  )
}
