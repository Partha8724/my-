import './globals.css'
import Link from 'next/link'

export const metadata = { title: 'WhaleScope' }

export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html className='dark'><body>
    <header className='border-b border-slate-800 bg-slate-950/90 sticky top-0 z-10'>
      <nav className='max-w-7xl mx-auto p-4 flex gap-4 items-center'>
        <Link href='/' className='font-bold text-cyan-300'>🐋 WhaleScope</Link>
        <Link href='/alerts'>Alerts</Link>
        <Link href='/signals'>Signals</Link>
        <Link href='/watchlist'>Watchlist</Link>
        <Link href='/settings'>Settings</Link>
        <span className='ml-auto text-xs px-2 py-1 rounded bg-amber-500/20 text-amber-300'>DEMO/LIVE badge</span>
      </nav>
    </header>
    <main className='max-w-7xl mx-auto p-4 space-y-4'>{children}</main>
  </body></html>
}
