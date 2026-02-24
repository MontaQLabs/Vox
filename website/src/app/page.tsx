import { Navigation } from '@/components/Navigation'
import { Hero } from '@/components/Hero'
import { Features } from '@/components/Features'
import { HowItWorks } from '@/components/HowItWorks'
import { Install } from '@/components/Install'
import { Footer } from '@/components/Footer'

export default function Home() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <Navigation />
      <Hero />
      <Features />
      <HowItWorks />
      <Install />
      <Footer />
    </div>
  )
}
