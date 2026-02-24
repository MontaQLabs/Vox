'use client'

import { useState, useEffect } from 'react'

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
      setIsOpen(false)
    }
  }

  const navItems = [
    { name: 'Features', id: 'features' },
    { name: 'Install', id: 'install' },
    { name: 'Docs', href: '/docs' },
    { name: 'GitHub', href: 'https://github.com/MontaQLabs/Vox' },
  ]

  return (
    <nav className={`nav ${scrolled ? 'scrolled' : ''}`} id="main-nav">
      <div style={{ padding: '0.625rem 1.125rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {/* Logo */}
          <a
            href="/"
            style={{
              display: 'flex', alignItems: 'center', gap: '0.5rem',
              textDecoration: 'none',
            }}
          >
            <div style={{
              width: '1.5rem', height: '1.5rem',
              background: 'var(--accent)', borderRadius: '0.3125rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '0.6875rem', fontWeight: 800, color: '#050506',
              fontFamily: '"Space Grotesk", sans-serif',
            }}>V</div>
            <span style={{
              fontSize: '0.9375rem', fontWeight: 600, color: 'var(--text-primary)',
              fontFamily: '"Space Grotesk", sans-serif',
              letterSpacing: '-0.02em',
            }}>Vox</span>
          </a>

          {/* Desktop links */}
          <div className="hidden-mobile" style={{ gap: '1.75rem', alignItems: 'center' }}>
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href || `#${item.id}`}
                onClick={(e) => {
                  if (!item.href) {
                    e.preventDefault()
                    scrollToSection(item.id!)
                  }
                }}
                style={{
                  fontSize: '0.75rem', color: 'var(--text-muted)',
                  textDecoration: 'none', transition: 'color 0.2s ease',
                  fontWeight: 500, letterSpacing: '0.01em',
                }}
                onMouseEnter={(e) => e.currentTarget.style.color = 'var(--text-primary)'}
                onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
              >
                {item.name}
              </a>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            className="mobile-only"
            onClick={() => setIsOpen(!isOpen)}
            style={{
              background: 'none', border: 'none', cursor: 'pointer',
              padding: '0.25rem', color: 'var(--text-secondary)',
              alignItems: 'center', justifyContent: 'center',
            }}
            aria-label="Toggle menu"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              {isOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
              ) : (
                <path d="M3 12h18M3 6h18M3 18h18" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div style={{
            paddingTop: '0.625rem',
            borderTop: '1px solid var(--border)',
            marginTop: '0.625rem',
            display: 'flex', flexDirection: 'column', gap: '0.125rem',
          }}>
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href || `#${item.id}`}
                onClick={(e) => {
                  if (!item.href) {
                    e.preventDefault()
                    scrollToSection(item.id!)
                  }
                }}
                style={{
                  padding: '0.5rem 0.625rem',
                  fontSize: '0.8125rem', color: 'var(--text-secondary)',
                  textDecoration: 'none', borderRadius: 'var(--radius-sm)',
                  transition: 'all 0.2s ease',
                }}
              >
                {item.name}
              </a>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
