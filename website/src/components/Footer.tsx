'use client'

export function Footer() {
  const linkStyle = {
    fontSize: '0.8125rem',
    color: 'var(--text-muted)',
    textDecoration: 'none' as const,
    transition: 'color 0.2s ease',
  }

  return (
    <footer style={{
      borderTop: '1px solid var(--border)',
      background: 'var(--bg-secondary)',
    }}>
      <div className="container" style={{ paddingTop: '2.5rem', paddingBottom: '1.5rem' }}>
        {/* Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '2rem 1.5rem',
          marginBottom: '2rem',
        }}>
          <style>{`
            @media (min-width: 768px) {
              .footer-grid-inner { grid-template-columns: 2fr 1fr 1fr 1fr !important; }
            }
          `}</style>
          <div className="footer-grid-inner" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '2rem 1.5rem',
            gridColumn: '1 / -1',
          }}>
            {/* Brand */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.625rem' }}>
                <div style={{
                  width: '1.375rem', height: '1.375rem',
                  background: 'var(--accent)', borderRadius: '0.25rem',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '0.5625rem', fontWeight: 800, color: '#050506',
                }}>V</div>
                <span style={{ fontWeight: 600, fontSize: '0.8125rem', color: 'var(--text-primary)' }}>Vox</span>
              </div>
              <p style={{
                fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.6, maxWidth: '220px',
              }}>
                Agent-to-Agent Communication Protocol.{' '}
                <a href="https://montaq.org" style={{ color: 'var(--text-tertiary)' }}>Montaq Labs</a>
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 style={{
                fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)',
                textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem',
              }}>Product</h4>
              <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                {[
                  { label: 'Features', href: '#features' },
                  { label: 'Install', href: '#install' },
                  { label: 'Docs', href: '/docs' },
                ].map(item => (
                  <li key={item.label}>
                    <a href={item.href} style={linkStyle}
                      onMouseEnter={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                      onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
                    >{item.label}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 style={{
                fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)',
                textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem',
              }}>Resources</h4>
              <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                {[
                  { label: 'GitHub', href: 'https://github.com/MontaQLabs/Vox' },
                  { label: 'PyPI', href: 'https://pypi.org/project/vox-communication' },
                  { label: 'Matrix.org', href: 'https://matrix.org' },
                ].map(item => (
                  <li key={item.label}>
                    <a href={item.href} style={linkStyle}
                      onMouseEnter={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                      onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
                    >{item.label}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 style={{
                fontSize: '0.6875rem', fontWeight: 600, color: 'var(--text-muted)',
                textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem',
              }}>Company</h4>
              <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                {[
                  { label: 'Montaq Labs', href: 'https://montaq.org' },
                  { label: 'Contact', href: 'mailto:team@vox.pm' },
                ].map(item => (
                  <li key={item.label}>
                    <a href={item.href} style={linkStyle}
                      onMouseEnter={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                      onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
                    >{item.label}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div style={{
          borderTop: '1px solid var(--border)',
          paddingTop: '1.25rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '0.5rem',
        }}>
          <p style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', margin: 0 }}>
            &copy; 2026 Montaq Labs. MIT License.
          </p>
          <p style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', margin: 0 }}>
            Built for AI agents.
          </p>
        </div>
      </div>
    </footer>
  )
}
