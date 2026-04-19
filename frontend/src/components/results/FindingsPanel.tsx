'use client'
import { useState, useMemo } from 'react'
import { clsx } from 'clsx'
import { Globe, Server, Building2, Filter } from 'lucide-react'
import FindingCard from './FindingCard'
import { EmptyState } from '@/components/ui'
import type { Finding, Category, RiskLevel } from '@/types'

interface Props { findings: Finding[] }

type Tab = 'all' | Category
const TABS: { id: Tab; label: string; icon: React.FC<{ className?: string }> }[] = [
  { id: 'all',        label: 'All',        icon: Filter },
  { id: 'social',     label: 'Social',     icon: Globe },
  { id: 'technical',  label: 'Technical',  icon: Server },
  { id: 'regulatory', label: 'Regulatory', icon: Building2 },
]

const RISK_FILTERS: { value: 'all' | RiskLevel; label: string; dot: string }[] = [
  { value: 'all',     label: 'All risks',  dot: 'bg-slate-500' },
  { value: 'high',    label: 'High',       dot: 'bg-red-400' },
  { value: 'medium',  label: 'Medium',     dot: 'bg-amber-400' },
  { value: 'low',     label: 'Low',        dot: 'bg-emerald-400' },
]

export default function FindingsPanel({ findings }: Props) {
  const [activeTab,  setActiveTab]  = useState<Tab>('all')
  const [riskFilter, setRiskFilter] = useState<'all' | RiskLevel>('all')

  const filtered = useMemo(() => {
    return findings.filter((f) => {
      const catMatch  = activeTab === 'all' || f.category === activeTab
      const riskMatch = riskFilter === 'all' || f.risk_level === riskFilter
      return catMatch && riskMatch
    })
  }, [findings, activeTab, riskFilter])

  const countFor = (tab: Tab) =>
    tab === 'all' ? findings.length : findings.filter((f) => f.category === tab).length

  return (
    <div>
      {/* Tabs */}
      <div className="flex items-center gap-1 mb-4 overflow-x-auto pb-1">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={clsx(
              'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-all duration-150',
              activeTab === id
                ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            )}
          >
            <Icon className="w-3.5 h-3.5" />
            {label}
            <span className={clsx(
              'text-xs px-1.5 py-0.5 rounded-full',
              activeTab === id ? 'bg-brand-500/20 text-brand-300' : 'bg-slate-700 text-slate-500'
            )}>
              {countFor(id)}
            </span>
          </button>
        ))}

        <div className="ml-auto flex items-center gap-1">
          {RISK_FILTERS.map(({ value, label, dot }) => (
            <button
              key={value}
              onClick={() => setRiskFilter(value)}
              className={clsx(
                'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all',
                riskFilter === value
                  ? 'bg-slate-700 text-slate-200'
                  : 'text-slate-500 hover:text-slate-300'
              )}
            >
              <span className={clsx('w-1.5 h-1.5 rounded-full', dot)} />
              {label}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <EmptyState
          icon={Filter}
          title="No findings match your filters"
          description="Try adjusting the category or risk level filter."
        />
      ) : (
        <div className="space-y-3">
          {filtered.map((finding, i) => (
            <FindingCard key={finding.id} finding={finding} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
