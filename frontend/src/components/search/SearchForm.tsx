'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { clsx } from 'clsx'
import { Search, Building2, User, Loader2, ChevronRight } from 'lucide-react'
import { useOSINT } from '@/context/OSINTContext'
import type { EntityType } from '@/types'

const EXAMPLES = {
  company:    ['OpenAI', 'Stripe', 'Anthropic', 'Vercel', 'Cloudflare'],
  individual: ['Elon Musk', 'Sam Altman', 'Linus Torvalds', 'Jensen Huang'],
}

export default function SearchForm() {
  const [query, setQuery]           = useState('')
  const [entityType, setEntityType] = useState<EntityType>('company')
  const { runSearch, isSearching }  = useOSINT()
  const router                      = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || isSearching) return
    const result = await runSearch({ query: query.trim(), entity_type: entityType })
    if (result) router.push(`/results/${result.id}`)
  }

  const handleExample = (q: string) => {
    setQuery(q)
  }

  return (
    <div className="w-full max-w-2xl mx-auto animate-slide-up">

      <div className="flex items-center justify-center gap-2 mb-6">
        {(['company', 'individual'] as EntityType[]).map((type) => {
          const Icon = type === 'company' ? Building2 : User
          return (
            <button
              key={type}
              onClick={() => setEntityType(type)}
              className={clsx(
                'flex items-center gap-2 px-5 py-2 rounded-full text-sm font-medium transition-all duration-200 border',
                entityType === type
                  ? 'bg-brand-600 text-white border-brand-500 shadow-lg shadow-brand-900/40'
                  : 'text-slate-400 border-slate-700 hover:border-slate-500 hover:text-slate-200'
              )}
            >
              <Icon className="w-4 h-4" />
              {type === 'company' ? 'Company' : 'Individual'}
            </button>
          )
        })}
      </div>

      <form onSubmit={handleSubmit} className="relative group">
        <div className={clsx(
          'relative flex items-center rounded-2xl border transition-all duration-300',
          'bg-slate-900/80 backdrop-blur-sm',
          isSearching
            ? 'border-brand-500/60 shadow-lg shadow-brand-900/30'
            : 'border-slate-700 hover:border-slate-500 focus-within:border-brand-500/60 focus-within:shadow-lg focus-within:shadow-brand-900/30'
        )}>
          <Search className="absolute left-4 w-5 h-5 text-slate-500 pointer-events-none" />

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={entityType === 'company' ? 'Enter company name…' : 'Enter full name…'}
            disabled={isSearching}
            className="w-full bg-transparent pl-12 pr-4 py-4 text-slate-100 placeholder-slate-500
                       text-lg focus:outline-none disabled:opacity-60"
          />

          <button
            type="submit"
            disabled={!query.trim() || isSearching}
            className={clsx(
              'mr-2 flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm',
              'transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed',
              'bg-brand-600 hover:bg-brand-500 text-white shadow-md',
              'focus:outline-none focus:ring-2 focus:ring-brand-500/50'
            )}
          >
            {isSearching
              ? <><Loader2 className="w-4 h-4 animate-spin" /> Scanning…</>
              : <><span>Search</span><ChevronRight className="w-4 h-4" /></>
            }
          </button>
        </div>
      </form>

      <div className="mt-5 flex flex-wrap justify-center gap-2">
        <span className="text-xs text-slate-600 self-center">Try:</span>
        {EXAMPLES[entityType].map((ex) => (
          <button
            key={ex}
            onClick={() => handleExample(ex)}
            disabled={isSearching}
            className="text-xs px-3 py-1.5 rounded-full border border-slate-700/60 text-slate-400
                       hover:border-brand-500/40 hover:text-brand-300 transition-all duration-150
                       disabled:opacity-40"
          >
            {ex}
          </button>
        ))}
      </div>

      {isSearching && (
        <div className="mt-8 space-y-2 animate-fade-in">
          {[
            'Querying social footprint…',
            'Checking technical infrastructure…',
            'Scanning regulatory databases…',
            'Running entity resolution…',
          ].map((msg, i) => (
            <div key={i} className="flex items-center gap-3 text-sm text-slate-500 px-2"
                 style={{ animationDelay: `${i * 0.4}s` }}>
              <div className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-pulse-slow" />
              {msg}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
