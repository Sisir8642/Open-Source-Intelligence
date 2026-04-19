'use client'
import { useState } from 'react'
import { format } from 'date-fns'
import { ExternalLink, ChevronDown, ChevronUp, Code2 } from 'lucide-react'
import { clsx } from 'clsx'
import { RiskBadge, ConfidenceBar, AdapterIcon, MockBadge } from '@/components/ui'
import type { Finding } from '@/types'

interface Props { finding: Finding; index: number }

const ADAPTER_LABELS: Record<string, string> = {
  google_search:  'Google Search',
  github:         'GitHub',
  newsapi:        'NewsAPI',
  opencorporates: 'OpenCorporates',
  twitter:        'Twitter / X',
  linkedin:       'LinkedIn',
  hibp:           'HaveIBeenPwned',
  whois:          'WHOIS',
  dns:            'DNS Records',
}

export default function FindingCard({ finding, index }: Props) {
  const [expanded, setExpanded]   = useState(false)
  const [showRaw, setShowRaw]     = useState(false)
  const label = ADAPTER_LABELS[finding.adapter] ?? finding.adapter

  return (
    <div
      className={clsx(
        'glass rounded-xl border transition-all duration-200 animate-fade-in overflow-hidden',
        finding.risk_level === 'high'
          ? 'border-red-500/20 hover:border-red-500/40'
          : finding.risk_level === 'medium'
          ? 'border-amber-500/20 hover:border-amber-500/30'
          : 'border-slate-700/50 hover:border-slate-600/60'
      )}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div
        className="flex items-start gap-3 p-4 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="mt-0.5 w-8 h-8 rounded-lg bg-slate-800 border border-slate-700/60 flex items-center justify-center shrink-0">
          <AdapterIcon adapter={finding.adapter} className="text-slate-400" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="text-xs font-medium text-slate-500">{label}</span>
            <RiskBadge level={finding.risk_level} />
            {finding.is_mock && <MockBadge />}
          </div>
          <h3 className="text-sm font-medium text-slate-200 leading-snug line-clamp-2">
            {finding.title}
          </h3>
        </div>

        <button className="text-slate-600 hover:text-slate-400 transition-colors shrink-0 mt-0.5">
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {expanded && (
        <div className="px-4 pb-4 border-t border-slate-800/80 pt-3 animate-fade-in">

          {finding.description && (
            <p className="text-sm text-slate-400 leading-relaxed mb-4">
              {finding.description}
            </p>
          )}

          <div className="grid grid-cols-2 gap-3 mb-4">
            <div>
              <div className="text-xs text-slate-600 mb-1">Confidence</div>
              <ConfidenceBar value={finding.confidence} />
            </div>
            <div>
              <div className="text-xs text-slate-600 mb-1">Fetched</div>
              <div className="text-xs text-slate-400">
                {format(new Date(finding.fetched_at), 'MMM d, HH:mm')}
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {finding.source_url && (
              <a
                href={finding.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary flex items-center gap-1.5"
                onClick={(e) => e.stopPropagation()}
              >
                <ExternalLink className="w-3.5 h-3.5" />
                View source
              </a>
            )}
            {finding.raw_data && (
              <button
                onClick={(e) => { e.stopPropagation(); setShowRaw(!showRaw) }}
                className="btn-secondary flex items-center gap-1.5"
              >
                <Code2 className="w-3.5 h-3.5" />
                {showRaw ? 'Hide' : 'Raw'} data
              </button>
            )}
          </div>

          {showRaw && finding.raw_data && (
            <pre className="mt-3 p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-400
                            font-mono overflow-auto max-h-48 animate-fade-in">
              {JSON.stringify(finding.raw_data, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}
