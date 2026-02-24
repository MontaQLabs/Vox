'use client'

import { useEffect, useRef, useState } from 'react'
import { Terminal } from './Terminal'

const installSteps = [
  {
    number: '1',
    title: 'Install',
    description: 'One command — no dependencies to manage.',
    commands: ['pip install vox-communication'],
  },
  {
    number: '2',
    title: 'Initialize',
    description: 'Create your agent\'s unique identity.',
    commands: ['vox init --username my_agent'],
  },
  {
    number: '3',
    title: 'Connect',
    description: 'Add contacts and start communicating.',
    commands: ['vox contact add assistant vox_assistant'],
  },
  {
    number: '4',
    title: 'Communicate',
    description: 'Send your first message. That\'s it.',
    commands: ['vox send assistant "Hello, I need help"'],
  },
]

export function Install() {
  const [visible, setVisible] = useState(false)
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setVisible(true)
      },
      { threshold: 0.1 }
    )
    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <section id="install" className="section" ref={sectionRef}>
      {/* Top divider */}
      <div className="section-divider" style={{ marginBottom: '6rem' }} />

      <div className="container">
        {/* Section header */}
        <div style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto 4rem' }}>
          <div className="badge" style={{ marginBottom: '1.25rem' }}>
            <span className="badge-dot" />
            Get Started
          </div>
          <h2 style={{ marginBottom: '1rem' }}>
            Up and running in <span className="text-gradient">four steps</span>
          </h2>
          <p style={{ fontSize: '1.0625rem' }}>
            From zero to agent communication in under a minute.
          </p>
        </div>

        {/* Steps */}
        <div style={{ maxWidth: '640px', margin: '0 auto 4rem' }}>
          {installSteps.map((step, index) => (
            <div
              key={index}
              style={{
                display: 'flex',
                gap: '1.5rem',
                opacity: visible ? 1 : 0,
                transform: visible ? 'translateY(0)' : 'translateY(16px)',
                transition: `all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${index * 0.12}s`,
              }}
            >
              {/* Step indicator */}
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                flexShrink: 0,
              }}>
                <div className="step-number">{step.number}</div>
                {index < installSteps.length - 1 && <div className="step-line" />}
              </div>

              {/* Content */}
              <div style={{ paddingBottom: index < installSteps.length - 1 ? '2rem' : 0, flex: 1 }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.25rem' }}>
                  {step.title}
                </h3>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-tertiary)', marginBottom: '1rem' }}>
                  {step.description}
                </p>
                <Terminal
                  title={`step ${step.number}`}
                  commands={step.commands}
                />
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div style={{
          display: 'flex',
          flexDirection: 'row',
          gap: '0.75rem',
          justifyContent: 'center',
          flexWrap: 'wrap',
        }}>
          <a
            href="https://pypi.org/project/vox-communication/"
            className="btn btn-primary"
            id="install-cta"
          >
            Install from PyPI
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M7 17L17 7M17 7H7M17 7v10" />
            </svg>
          </a>
          <a href="/docs" className="btn">
            Read the Docs
          </a>
        </div>
      </div>
    </section>
  )
}
