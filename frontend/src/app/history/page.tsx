'use client'
import { useEffect } from 'react'
import Link from 'next/link'
import { format } from 'date-fns'
import { History, Trash2, ExternalLink, Building2, User, Search } from 'lucide-react'
import Navbar from '@/components/layout/Navbar'
import { RiskBadge, Spinner, EmptyState } from '@/components/ui'
import { useOSINT } from '@/context/OSINTContext'
import { clsx } from 'clsx'

export default function HistoryPage() {
  const { history, isLoadingHistory, loadHistory, deleteSearch } = useOSINT()

  useEffect(() => { loadHistory() }, [])

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.preventDefault()
    e.stopPropagation()
    if (confirm('Delete this search and all its findings?')) {
      await deleteSearch(id)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8">

        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <History className="w-5 h-5 text-brand-400" />
              Search History
            </h1>
            <p className="text-slate-500 text-sm mt-1">All past intelligence searches stored in your database</p>
          </div>

          <Link href="/" className="btn-primary flex items-center gap-2 text-sm">
            <Search className="w-4 h-4" />
            New search
          </Link>
        </div>

        {isLoadingHistory ? (
          <div className="flex items-center justify-center py-20">
            <Spinner className="w-7 h-7 text-brand-400" />
          </div>
        ) : history.length === 0 ? (
          <EmptyState
            icon={History}
            title="No searches yet"
            description="Run your first intelligence search to see it appear here."
          />
        ) : (
          <div className="space-y-2">
            {history.map((item, i) => {
              const Icon = item.entity_type === 'company' ? Building2 : User
              return (
                <Link
                  key={item.id}
                  href={`/results/${item.id}`}
                  className={clsx(
                    'group flex items-center gap-4 p-4 rounded-xl border transition-all duration-200',
                    'glass glass-hover animate-fade-in'
                  )}
                  style={{ animationDelay: `${i * 40}ms` }}
                >
                  <div className="w-9 h-9 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                    <Icon className="w-4 h-4 text-slate-400" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-medium text-slate-200 truncate">{item.query}</span>
                      <span className="text-xs text-slate-600 capitalize">{item.entity_type}</span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                      <span>{item.finding_count} findings</span>
                      <span>·</span>
                      <span>{format(new Date(item.created_at), 'MMM d, yyyy HH:mm')}</span>
                      {item.status === 'failed' && (
                        <><span>·</span><span className="text-red-400">Partial</span></>
                      )}
                    </div>
                  </div>

                  <div className="shrink-0">
                    <RiskBadge level={item.risk_level} />
                  </div>

                  <div className="flex items-center gap-1 shrink-0">
                    <button
                      onClick={(e) => handleDelete(e, item.id)}
                      className="p-2 rounded-lg text-slate-600 hover:text-red-400 hover:bg-red-500/10 transition-all opacity-0 group-hover:opacity-100"
                      title="Delete"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                    <div className="p-2 text-slate-600 group-hover:text-brand-400 transition-colors">
                      <ExternalLink className="w-3.5 h-3.5" />
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
        )}

      </main>
    </div>
  )
}
