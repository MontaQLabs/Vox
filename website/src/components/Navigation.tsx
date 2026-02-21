'use client'

import { useState } from 'react'

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
      setIsOpen(false)
    }
  }

  return (
    <nav className="nav">
      <div className="container">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-foreground rounded"></div>
            <span className="text-xl font-semibold">Vox</span>
          </div>
          
          <div className="hidden md:flex gap-8">
            {[
              { name: 'Features', id: 'features' },
              { name: 'Install', id: 'install' },
              { name: 'Docs', href: 'https://docs.vox.pm' },
              { name: 'GitHub', href: 'https://github.com/vox/vox' }
            ].map((item) => (
              <a
                key={item.name}
                href={item.href || `#${item.id}`}
                onClick={(e) => {
                  if (!item.href) {
                    e.preventDefault()
                    scrollToSection(item.id!)
                  }
                }}
                className="text-sm transition-colors hover:text-muted-foreground"
              >
                {item.name}
              </a>
            ))}
          </div>
          
          <button
            className="md:hidden"
            onClick={() => setIsOpen(!isOpen)}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              {isOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
              ) : (
                <path d="M3 12h18M3 6h18M3 18h18" />
              )}
            </svg>
          </button>
        </div>
        
        {isOpen && (
          <div className="md:hidden py-4 space-y-2">
            {[
              { name: 'Features', id: 'features' },
              { name: 'Install', id: 'install' },
              { name: 'Docs', href: 'https://docs.vox.pm' },
              { name: 'GitHub', href: 'https://github.com/vox/vox' }
            ].map((item) => (
              <a
                key={item.name}
                href={item.href || `#${item.id}`}
                onClick={(e) => {
                  if (!item.href) {
                    e.preventDefault()
                    scrollToSection(item.id!)
                  }
                }}
                className="block py-2 text-sm transition-colors hover:text-muted-foreground"
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
