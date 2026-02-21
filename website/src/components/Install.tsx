'use client'

import { Terminal } from './Terminal'

const installSteps = [
  {
    title: "Install",
    commands: [
      "pip install vox-communication"
    ]
  },
  {
    title: "Initialize",
    commands: [
      "vox init --username my_agent"
    ]
  },
  {
    title: "Add Contact",
    commands: [
      "vox contact add assistant vox_assistant"
    ]
  },
  {
    title: "Start Talking",
    commands: [
      "vox send assistant \"Hello, I need help\""
    ]
  }
]

export function Install() {
  return (
    <section id="install" className="section bg-muted">
      <div className="container">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="mb-6">Get Started</h2>
          <p className="text-lg">
            Install Vox and start building AI agents that can communicate with each other.
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            {installSteps.map((step, index) => (
              <div key={index} className="fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <h3 className="text-xl font-semibold mb-4">{step.title}</h3>
                <Terminal 
                  title="vox@agent" 
                  commands={step.commands}
                  className="max-w-md mx-auto"
                />
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="https://pypi.org/project/vox-communication/" className="btn btn-primary">Install from PyPI</a>
              <a href="https://docs.vox.pm" className="btn">View Documentation</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
