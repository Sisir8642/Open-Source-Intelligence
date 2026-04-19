'use client'
import { format } from 'date-fns'
import { Building2, User, Clock, CheckCircle2, AlertTriangle } from 'lucide-react'
import { RiskBadge, RiskScoreRing, ConfidenceBar } from '@/components/ui'
import type { Search } from '@/types'

interface Props { search: Search }

const CATEGORY_LABELS = {
  social:     { label: 'Social',     color: 'text-violet-400', bg: 'bg-violet-500/10' },
  technical:  { label: 'Technical',  color: 'text-cyan-400',   bg: 'bg-cyan-500/10' },
  regulatory: { label: 'Regulatory', color: 'text-amber-400',  bg: 'bg-amber-500/10' },
}

export default function SearchHeader({ search }: Props) {
  const Icon   = search.entity_type === 'company' ? Building2 : User
  const counts = search.findings.reduce<Record<string, number>>((acc, f) => {
    acc[f.category] = (acc[f.category] ?? 0) + 1
    return acc
  }, {})

  return (
    <div className="card mb-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-start gap-5">

        {/* Entity info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-7 h-7 rounded-lg bg-brand-600/20 border border-brand-500/20 flex items-center justify-center">
              <Icon className="w-3.5 h-3.5 text-brand-400" />
            </div>
            <span className="text-xs text-slate-500 uppercase tracking-widest font-medium">
              {search.entity_type}
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight truncate">
            {search.query}
          </h1>

          {search.summary && (
            <p className="mt-2 text-sm text-slate-400 leading-relaxed max-w-xl">
              {search.summary}
            </p>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-3">
            <RiskBadge level={search.risk_level} size="md" />

            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-slate-600" />
              {search.findings.length} findings
            </span>

            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <Clock className="w-3.5 h-3.5 text-slate-600" />
              {search.completed_at
                ? format(new Date(search.completed_at), 'MMM d, yyyy HH:mm')
                : format(new Date(search.created_at), 'MMM d, yyyy HH:mm')}
            </span>

            {search.status === 'failed' && (
              <span className="flex items-center gap-1 text-xs text-red-400">
                <AlertTriangle className="w-3.5 h-3.5" />
                Partial results
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-col items-center gap-2 shrink-0">
          <RiskScoreRing score={search.risk_score} level={search.risk_level} />
          <div className="text-center">
            <div className="text-xs text-slate-500 mb-1.5">Confidence</div>
            <ConfidenceBar value={search.confidence_score} />
          </div>
        </div>
      </div>

      <div className="mt-5 pt-4 border-t border-slate-800 grid grid-cols-3 gap-3">
        {Object.entries(CATEGORY_LABELS).map(([cat, cfg]) => (
          <div key={cat} className={`rounded-lg ${cfg.bg} px-3 py-2.5 text-center`}>
            <div className={`text-lg font-bold ${cfg.color}`}>{counts[cat] ?? 0}</div>
            <div className="text-xs text-slate-500 mt-0.5">{cfg.label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
