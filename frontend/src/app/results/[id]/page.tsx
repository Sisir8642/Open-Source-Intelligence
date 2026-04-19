'use client'
import { useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, RefreshCw } from 'lucide-react'
import Navbar from '@/components/layout/Navbar'
import SearchHeader from '@/components/results/SearchHeader'
import FindingsPanel from '@/components/results/FindingsPanel'
import ExportPanel from '@/components/export/ExportPanel'
import { Spinner, EmptyState } from '@/components/ui'
import { useOSINT } from '@/context/OSINTContext'
import { Search } from 'lucide-react'

export default function ResultsPage() {
  const params             = useParams()
  const router             = useRouter()
  const id                 = params?.id as string
  const { currentSearch, loadSearch, isSearching } = useOSINT()

  useEffect(() => {
    if (id && (!currentSearch || currentSearch.id !== id)) {
      loadSearch(id)
    }
  }, [id])

  const search = currentSearch?.id === id ? currentSearch : null

  // Loading
  if (!search && !isSearching) {
    return (
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <Spinner className="w-8 h-8 text-brand-400 mx-auto mb-4" />
            <p className="text-slate-500 text-sm">Loading intelligence report…</p>
          </div>
        </div>
      </div>
    )
  }

  if (!search) {
    return (
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <EmptyState
            icon={Search}
            title="Search not found"
            description="This search may have been deleted or doesn't exist."
          />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8">

        <div className="flex items-center justify-between mb-6">
          <Link
            href="/"
            className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-300 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            New search
          </Link>

          <Link
            href="/history"
            className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-300 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            History
          </Link>
        </div>

        <SearchHeader search={search} />

        <div className="mb-2">
          <h2 className="section-header">Intelligence Findings</h2>
        </div>
        <FindingsPanel findings={search.findings ?? []} />

        <ExportPanel searchId={search.id} />

      </main>
    </div>
  )
}
