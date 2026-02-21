import { Navigation } from '@/components/Navigation'
import { Hero } from '@/components/Hero'
import { Features } from '@/components/Features'
import { Install } from '@/components/Install'
import { Footer } from '@/components/Footer'

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <Hero />
      <Features />
      <Install />
      <Footer />
    </div>
  )
}
