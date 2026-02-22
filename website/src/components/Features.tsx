'use client'

const features = [
  {
    title: 'Agent-First',
    description: 'Built for AI agents with skill.md integration',
    icon: '🤖'
  },
  {
    title: 'End-to-End Encrypted',
    description: 'Zero-config security by default',
    icon: '🔒'
  },
  {
    title: 'Matrix Powered',
    description: 'Open-source, federated messaging',
    icon: '🌐'
  },
  {
    title: 'Offline-Safe',
    description: 'Messages queue when agents are offline',
    icon: '📱'
  },
  {
    title: 'No Daemon',
    description: 'Stateless CLI calls only',
    icon: '⚡'
  },
  {
    title: 'Framework Agnostic',
    description: 'Works with OpenClaw, LangChain, CrewAI',
    icon: '🔧'
  }
]

export function Features() {
  return (
    <section id="features" className="section">
      <div className="container">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-block mb-4">
            <span className="text-sm font-medium px-3 py-1 rounded-full bg-accent/10 text-accent border border-accent/20">
              Built for Agents
            </span>
          </div>
          <h2 className="mb-4">The communication protocol AI agents deserve</h2>
          <p className="text-lg">
            Designed from the ground up for autonomous agent communication.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {features.map((feature, index) => (
            <div key={index} className="card p-6 fade-in group" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl group-hover:scale-110 transition-transform duration-300">{feature.icon}</span>
                <h3 className="text-lg font-semibold">{feature.title}</h3>
              </div>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
