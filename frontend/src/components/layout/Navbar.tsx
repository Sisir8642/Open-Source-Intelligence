'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { clsx } from 'clsx'
import { Search, History, Shield, Zap } from 'lucide-react'

const NAV_LINKS = [
  { href: '/',        label: 'Search',  icon: Search },
  { href: '/history', label: 'History', icon: History },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">

          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-brand-600/20 border border-brand-500/30 flex items-center justify-center group-hover:bg-brand-600/30 transition-colors">
              <Shield className="w-4 h-4 text-brand-400" />
            </div>
            <span className="font-semibold text-slate-100 hidden sm:block">
              OSINT<span className="text-brand-400">Intel</span>
            </span>
          </Link>

          <nav className="flex items-center gap-1">
            {NAV_LINKS.map(({ href, label, icon: Icon }) => {
              const active = pathname === href
              return (
                <Link
                  key={href}
                  href={href}
                  className={clsx(
                    'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
                    active
                      ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{label}</span>
                </Link>
              )
            })}
          </nav>

          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <Zap className="w-3 h-3 text-brand-400" />
              <span className="hidden sm:inline">Live</span>
            </span>
          </div>

        </div>
      </div>
    </header>
  )
}
