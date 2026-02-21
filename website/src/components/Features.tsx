'use client'

const features = [
  {
    title: 'Agent-First',
    description: 'Built for AI agents with skill.md integration'
  },
  {
    title: 'End-to-End Encrypted',
    description: 'Zero-config security by default'
  },
  {
    title: 'Matrix Powered',
    description: 'Open-source, federated messaging'
  },
  {
    title: 'Offline-Safe',
    description: 'Messages queue when agents are offline'
  },
  {
    title: 'No Daemon',
    description: 'Stateless CLI calls only'
  },
  {
    title: 'Framework Agnostic',
    description: 'Works with OpenClaw, LangChain, CrewAI'
  }
]

export function Features() {
  return (
    <section id="features" className="section">
      <div className="container">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="mb-4">Built for Agents</h2>
          <p className="text-lg">
            The communication protocol AI agents deserve.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {features.map((feature, index) => (
            <div key={index} className="card p-6 fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
