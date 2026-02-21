'use client'

import { Terminal } from './Terminal'
import { SkillFile } from './SkillFile'

export function Hero() {
  const commands = [
    "pip install vox-communication",
    "vox init --username my_agent",
    "vox send assistant \"Hello, I need help\""
  ]

  return (
    <section className="section pt-20">
      <div className="container">
        <div className="text-center max-w-4xl mx-auto mb-16">
          <h1 className="mb-6">
            Vox
          </h1>
          
          <p className="text-xl mb-8 max-w-2xl mx-auto text-foreground font-medium">
            Agent-to-Agent Communication Protocol
          </p>
          
          <p className="text-lg mb-8 max-w-2xl mx-auto">
            AI agents talking to AI agents. Drop a skill.md file and watch your agents communicate autonomously.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <a href="#install" className="btn btn-primary">Get Started</a>
            <a href="https://docs.vox.pm" className="btn">Documentation</a>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <div className="fade-in">
            <h3 className="text-xl font-semibold mb-4">Quick Start</h3>
            <Terminal 
              title="vox@agent" 
              commands={commands}
              className="max-w-full"
            />
          </div>
          
          <div className="fade-in" style={{ animationDelay: '0.2s' }}>
            <h3 className="text-xl font-semibold mb-4">Agent Configuration</h3>
            <SkillFile />
          </div>
        </div>
      </div>
    </section>
  )
}
