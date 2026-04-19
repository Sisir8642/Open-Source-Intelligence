import Navbar from '@/components/layout/Navbar'
import SearchForm from '@/components/search/SearchForm'
import { Shield, Zap, Database, Lock } from 'lucide-react'

const FEATURES = [
  { icon: Shield,   title: 'Multi-vector intelligence',  desc: 'Social, technical, and regulatory sources in one scan' },
  { icon: Zap,      title: 'Real-time aggregation',      desc: 'All adapters run in parallel for instant results' },
  { icon: Database, title: 'Persistent history',         desc: 'Every search stored and retrievable for auditing' },
  { icon: Lock,     title: 'Risk scoring engine',        desc: 'Confidence-weighted severity across all findings' },
]

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 py-16">

        <div className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-brand-500/30 bg-brand-600/10 text-brand-300 text-xs font-medium mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-brand-400 animate-pulse" />
            Open-Source Intelligence Platform
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white tracking-tight mb-4">
            Intelligence at
            <span className="bg-gradient-to-r from-brand-400 to-violet-400 bg-clip-text text-transparent"> scale</span>
          </h1>

          <p className="text-slate-400 text-lg max-w-xl mx-auto leading-relaxed">
            Aggregate public intelligence on any company or individual from 9+ data sources.
            Entity-resolved, risk-scored, and export-ready.
          </p>
        </div>

        <SearchForm />

        <div className="mt-20 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl w-full">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="glass rounded-xl p-4 text-center hover:border-slate-600/60 transition-colors">
              <div className="w-9 h-9 rounded-lg bg-brand-600/15 border border-brand-500/20 flex items-center justify-center mx-auto mb-3">
                <Icon className="w-4 h-4 text-brand-400" />
              </div>
              <div className="text-xs font-medium text-slate-300 mb-1">{title}</div>
              <div className="text-xs text-slate-600 leading-relaxed">{desc}</div>
            </div>
          ))}
        </div>

      </main>

      <footer className="border-t border-slate-800/60 py-4 text-center text-xs text-slate-600">
        OSINT Intelligence Platform · Data sourced from public APIs · Simulated data clearly marked
      </footer>
    </div>
  )
}
