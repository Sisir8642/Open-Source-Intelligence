'use client'
import { clsx } from 'clsx'
import type { RiskLevel, Category } from '@/types'
import {
  Globe, Github, Newspaper, Building2,
  Twitter, Linkedin, ShieldAlert, Server,
  Search, Loader2, AlertTriangle, CheckCircle, Info,
} from 'lucide-react'

const RISK_CONFIG: Record<RiskLevel, { label: string; dot: string; cls: string }> = {
  high:    { label: 'High',    dot: 'bg-red-400',     cls: 'badge-risk-high' },
  medium:  { label: 'Medium',  dot: 'bg-amber-400',   cls: 'badge-risk-medium' },
  low:     { label: 'Low',     dot: 'bg-emerald-400', cls: 'badge-risk-low' },
  unknown: { label: 'Unknown', dot: 'bg-slate-500',   cls: 'badge-risk-unknown' },
}

export function RiskBadge({ level, size = 'sm' }: { level: RiskLevel; size?: 'sm' | 'md' | 'lg' }) {
  const cfg = RISK_CONFIG[level] ?? RISK_CONFIG.unknown
  return (
    <span className={clsx('badge', cfg.cls, size === 'lg' && 'text-sm px-3 py-1')}>
      <span className={clsx('w-1.5 h-1.5 rounded-full inline-block', cfg.dot)} />
      {cfg.label} Risk
    </span>
  )
}

export function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100)
  const color = pct >= 80 ? 'bg-emerald-500' : pct >= 50 ? 'bg-amber-500' : 'bg-red-500'
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={clsx('h-full rounded-full transition-all', color)} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs text-slate-400 w-8 text-right">{pct}%</span>
    </div>
  )
}

export function RiskScoreRing({ score, level }: { score: number; level: RiskLevel }) {
  const pct = Math.round(score * 100)
  const r = 36
  const circ = 2 * Math.PI * r
  const dash = circ * (1 - score)
  const strokeColor: Record<RiskLevel, string> = {
    high: '#f87171', medium: '#fbbf24', low: '#34d399', unknown: '#64748b',
  }
  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width="100" height="100" className="-rotate-90">
        <circle cx="50" cy="50" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="50" cy="50" r={r}
          fill="none"
          stroke={strokeColor[level]}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={dash}
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
      </svg>
      <div className="absolute text-center">
        <div className="text-xl font-bold text-white">{pct}</div>
        <div className="text-xs text-slate-400">risk</div>
      </div>
    </div>
  )
}

const ADAPTER_ICONS: Record<string, React.FC<{ className?: string }>> = {
  google_search: Globe,
  github: Github,
  newsapi: Newspaper,
  opencorporates: Building2,
  twitter: Twitter,
  linkedin: Linkedin,
  hibp: ShieldAlert,
  whois: Server,
  dns: Server,
}

const CATEGORY_ICONS: Record<Category, React.FC<{ className?: string }>> = {
  social: Globe,
  technical: Server,
  regulatory: Building2,
}

export function AdapterIcon({ adapter, className }: { adapter: string; className?: string }) {
  const Icon = ADAPTER_ICONS[adapter] ?? Search
  return <Icon className={clsx('w-4 h-4', className)} />
}

export function CategoryIcon({ category, className }: { category: Category; className?: string }) {
  const Icon = CATEGORY_ICONS[category] ?? Search
  return <Icon className={clsx('w-4 h-4', className)} />
}

export function Spinner({ className }: { className?: string }) {
  return <Loader2 className={clsx('animate-spin', className)} />
}

export function StatusIcon({ status }: { status: 'success' | 'warning' | 'info' | 'error' }) {
  const map = {
    success: <CheckCircle className="w-4 h-4 text-emerald-400" />,
    warning: <AlertTriangle className="w-4 h-4 text-amber-400" />,
    info:    <Info className="w-4 h-4 text-blue-400" />,
    error:   <AlertTriangle className="w-4 h-4 text-red-400" />,
  }
  return map[status]
}

export function EmptyState({ icon: Icon, title, description }: {
  icon: React.FC<{ className?: string }>
  title: string
  description?: string
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center mb-4">
        <Icon className="w-7 h-7 text-slate-500" />
      </div>
      <h3 className="text-slate-300 font-medium mb-1">{title}</h3>
      {description && <p className="text-slate-500 text-sm max-w-xs">{description}</p>}
    </div>
  )
}

export function MockBadge() {
  return (
    <span className="badge bg-slate-700/40 text-slate-500 border border-slate-600/30 text-xs">
      simulated
    </span>
  )
}
