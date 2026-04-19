'use client'
import { useState } from 'react'
import { FileText, FileCode2, Download, Loader2, CheckCircle2 } from 'lucide-react'
import { clsx } from 'clsx'
import { searchAPI, downloadReport } from '@/lib/api'
import toast from 'react-hot-toast'
import type { ReportFormat } from '@/types'

interface Props { searchId: string }

const FORMATS: { id: ReportFormat; label: string; desc: string; icon: React.FC<{ className?: string }> }[] = [
  {
    id: 'pdf',
    label: 'PDF Report',
    desc: 'Professional formatted report with risk scores and findings',
    icon: FileText,
  },
  {
    id: 'markdown',
    label: 'Markdown',
    desc: 'Plain text markdown — great for GitHub, Notion, or Obsidian',
    icon: FileCode2,
  },
]

export default function ExportPanel({ searchId }: Props) {
  const [loading, setLoading]     = useState<ReportFormat | null>(null)
  const [generated, setGenerated] = useState<Record<string, string>>({})

  const handleGenerate = async (format: ReportFormat) => {
    setLoading(format)
    try {
      const report = await searchAPI.generateReport(searchId, { format })
      setGenerated((prev) => ({ ...prev, [format]: report.id }))
      toast.success(`${format.toUpperCase()} report generated`)
    } catch {
      toast.error('Report generation failed')
    } finally {
      setLoading(null)
    }
  }

  const handleDownload = (format: ReportFormat) => {
    const reportId = generated[format]
    if (reportId) downloadReport(reportId)
  }

  return (
    <div className="card mt-6">
      <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
        <Download className="w-4 h-4 text-brand-400" />
        Export Report
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {FORMATS.map(({ id, label, desc, icon: Icon }) => {
          const isLoading   = loading === id
          const isDone      = !!generated[id]
          return (
            <div
              key={id}
              className={clsx(
                'rounded-xl border p-4 transition-all duration-200',
                isDone
                  ? 'border-emerald-500/30 bg-emerald-500/5'
                  : 'border-slate-700/50 bg-slate-800/30 hover:border-slate-600'
              )}
            >
              <div className="flex items-start gap-3 mb-3">
                <div className={clsx(
                  'w-9 h-9 rounded-lg flex items-center justify-center shrink-0',
                  isDone ? 'bg-emerald-500/15' : 'bg-slate-700/60'
                )}>
                  {isDone
                    ? <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    : <Icon className="w-4 h-4 text-slate-400" />
                  }
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">{label}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{desc}</div>
                </div>
              </div>

              {isDone ? (
                <button
                  onClick={() => handleDownload(id)}
                  className="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium
                             bg-emerald-500/15 text-emerald-300 hover:bg-emerald-500/25 transition-colors border border-emerald-500/20"
                >
                  <Download className="w-3.5 h-3.5" />
                  Download {label}
                </button>
              ) : (
                <button
                  onClick={() => handleGenerate(id)}
                  disabled={!!loading}
                  className={clsx(
                    'w-full flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium',
                    'btn-primary disabled:opacity-40'
                  )}
                >
                  {isLoading
                    ? <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Generating…</>
                    : <><FileText className="w-3.5 h-3.5" /> Generate {label}</>
                  }
                </button>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
