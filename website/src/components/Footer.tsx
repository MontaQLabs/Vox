'use client'

export function Footer() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="container py-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
          <div>
            <h3 className="font-semibold mb-3 text-sm">Vox</h3>
            <p className="text-xs text-muted-foreground">
              Agent-to-Agent Communication Protocol
            </p>
          </div>
          
          <div>
            <h4 className="font-medium mb-3 text-sm">Product</h4>
            <ul className="space-y-1 text-xs">
              <li><a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">Features</a></li>
              <li><a href="#install" className="text-muted-foreground hover:text-foreground transition-colors">Installation</a></li>
              <li><a href="/docs" className="text-muted-foreground hover:text-foreground transition-colors">Documentation</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium mb-3 text-sm">Resources</h4>
            <ul className="space-y-1 text-xs">
              <li><a href="https://github.com/vox/vox" className="text-muted-foreground hover:text-foreground transition-colors">GitHub</a></li>
              <li><a href="https://pypi.org/project/vox-communication" className="text-muted-foreground hover:text-foreground transition-colors">PyPI</a></li>
              <li><a href="https://matrix.org" className="text-muted-foreground hover:text-foreground transition-colors">Matrix.org</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium mb-3 text-sm">Company</h4>
            <ul className="space-y-1 text-xs">
              <li><a href="https://vox.pm" className="text-muted-foreground hover:text-foreground transition-colors">Website</a></li>
              <li><a href="mailto:team@vox.pm" className="text-muted-foreground hover:text-foreground transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-border pt-6 text-center">
          <p className="text-xs text-muted-foreground">
            &copy; 2026 Montaq Labs. Licensed under MIT License.
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Built with &hearts; for AI agents everywhere
          </p>
        </div>
      </div>
    </footer>
  )
}
