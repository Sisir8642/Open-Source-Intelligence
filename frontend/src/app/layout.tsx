import type { Metadata } from 'next'
import { Toaster } from 'react-hot-toast'
import { OSINTProvider } from '@/context/OSINTContext'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'OSINT Intelligence Platform',
  description: 'Open-source intelligence aggregation for companies and individuals',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        <OSINTProvider>
          {children}
          <Toaster
            position="bottom-right"
            toastOptions={{
              style: {
                background: '#1e293b',
                color: '#f1f5f9',
                border: '1px solid rgba(99,102,241,0.3)',
                borderRadius: '10px',
                fontSize: '14px',
              },
              success: { iconTheme: { primary: '#10b981', secondary: '#1e293b' } },
              error:   { iconTheme: { primary: '#ef4444', secondary: '#1e293b' } },
            }}
          />
        </OSINTProvider>
      </body>
    </html>
  )
}
