import './globals.css'
import Link from 'next/link'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="mx-auto max-w-7xl p-4">
          <header className="mb-4 flex flex-wrap gap-4">
            {['/', '/alerts', '/signals', '/watchlist', '/settings'].map((href) => (
              <Link key={href} className="rounded bg-slate-800 px-3 py-1" href={href}>{href === '/' ? 'dashboard' : href.slice(1)}</Link>
            ))}
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}
