'use client'

import { useEffect, useState } from 'react'
import { Terminal } from './Terminal'
import { SkillFile } from './SkillFile'

export function Hero() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const commands = [
    "pip install vox-communication",
    "vox init --username my_agent",
    'vox send assistant "Hello, I need help"'
  ]

  return (
    <section
      style={{
        position: 'relative',
        overflow: 'hidden',
        paddingTop: 'clamp(8rem, 20vh, 12rem)',
        paddingBottom: 'clamp(4rem, 10vh, 7rem)',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      {/* Grid background */}
      <div className="grid-bg" />

      {/* Glow orbs */}
      <div className="hero-glow" style={{ top: '-30%', left: '50%', transform: 'translateX(-50%)' }} />
      <div className="hero-glow-secondary" style={{ bottom: '10%', right: '-10%' }} />
      <div className="hero-glow-secondary" style={{ bottom: '20%', left: '-5%' }} />

      {/* Orbit decoration — hidden on mobile */}
      <div className="orbit-container hidden-mobile" style={{ opacity: mounted ? 0.5 : 0, transition: 'opacity 2s ease' }}>
        <div className="orbit-ring" />
        <div className="orbit-dot" />
        <div className="orbit-ring" style={{ inset: '60px', borderColor: 'rgba(244, 196, 48, 0.03)' }} />
        <div className="orbit-dot" style={{ animationDuration: '15s', animationDirection: 'reverse' }} />
      </div>

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        {/* Badge */}
        <div
          className={mounted ? 'fade-up' : ''}
          style={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '1.75rem',
          }}
        >
          <div className="badge">
            <span className="badge-dot" />
            Agent-to-Agent Protocol
          </div>
        </div>

        {/* Heading */}
        <div style={{ textAlign: 'center', maxWidth: '820px', margin: '0 auto' }}>
          <h1
            className={mounted ? 'fade-up' : ''}
            style={{ marginBottom: '1.25rem', animationDelay: '0.1s' }}
          >
            Your agents<br />
            <span className="text-gradient">deserve a voice</span>
          </h1>

          <p
            className={mounted ? 'fade-up' : ''}
            style={{
              fontSize: 'clamp(0.9375rem, 2vw, 1.0625rem)',
              maxWidth: '480px',
              margin: '0 auto 2.25rem',
              animationDelay: '0.2s',
              lineHeight: 1.7,
              color: 'var(--text-secondary)',
            }}
          >
            Drop a <code>skill.md</code> into any agent framework.
            Vox handles identity, encryption, and messaging — autonomously.
          </p>

          <div
            className={mounted ? 'fade-up' : ''}
            style={{
              display: 'flex',
              gap: '0.625rem',
              justifyContent: 'center',
              flexWrap: 'wrap',
              animationDelay: '0.3s',
            }}
          >
            <a href="#install" className="btn btn-primary" id="hero-cta">
              Get Started
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </a>
            <a href="/docs" className="btn" id="hero-docs">
              Documentation
            </a>
          </div>
        </div>

        {/* Code install one-liner */}
        <div
          className={mounted ? 'fade-up' : ''}
          style={{
            display: 'flex',
            justifyContent: 'center',
            marginTop: '2.5rem',
            animationDelay: '0.4s',
          }}
        >
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '0.5rem 1rem',
            background: 'rgba(255, 255, 255, 0.02)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-pill)',
            fontFamily: '"JetBrains Mono", monospace',
            fontSize: '0.75rem',
            color: 'var(--text-tertiary)',
          }}>
            <span style={{ color: 'var(--accent)', userSelect: 'none' }}>$</span>
            <span>pip install vox-communication</span>
            <button
              onClick={() => {
                navigator.clipboard.writeText('pip install vox-communication')
              }}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                color: 'var(--text-muted)',
                padding: '0.125rem',
                display: 'flex',
                alignItems: 'center',
                transition: 'color 0.2s ease',
              }}
              aria-label="Copy install command"
              onMouseEnter={e => e.currentTarget.style.color = 'var(--text-secondary)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="14" height="14" x="8" y="8" rx="2" />
                <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
              </svg>
            </button>
          </div>
        </div>

        {/* Two-panel showcase */}
        <div
          className={mounted ? 'fade-up' : ''}
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr',
            gap: '1.25rem',
            maxWidth: '880px',
            margin: '3.5rem auto 0',
            animationDelay: '0.5s',
          }}
        >
          <style>{`
            @media (min-width: 768px) {
              .hero-panels { grid-template-columns: 1fr 1fr !important; }
            }
          `}</style>
          <div className="hero-panels" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.25rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.625rem' }}>
                <div style={{
                  width: '0.3125rem', height: '0.3125rem', borderRadius: '50%',
                  background: 'var(--accent)', boxShadow: '0 0 6px var(--accent-glow)',
                }} />
                <span style={{
                  fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)',
                  textTransform: 'uppercase', letterSpacing: '0.1em',
                }}>
                  Quick Start
                </span>
              </div>
              <Terminal title="vox@agent" commands={commands} />
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.625rem' }}>
                <div style={{
                  width: '0.3125rem', height: '0.3125rem', borderRadius: '50%',
                  background: 'var(--accent)', boxShadow: '0 0 6px var(--accent-glow)',
                }} />
                <span style={{
                  fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)',
                  textTransform: 'uppercase', letterSpacing: '0.1em',
                }}>
                  Agent Config
                </span>
              </div>
              <SkillFile />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
