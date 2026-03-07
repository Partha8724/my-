import Link from 'next/link'
import { fetchJson } from '@/lib/api'
import { ProviderBadge } from '@/components/ProviderBadge'
import { AlertTicker } from '@/components/AlertTicker'

type Overview = { symbol: string; price: number; change_24h: number; volume: number; pressure: number }

type Provider = { provider: string; healthy: boolean; mode: string }

export default async function Dashboard() {
  const [overview, providers, alerts, signals] = await Promise.all([
    fetchJson<Overview[]>('/api/market/overview').catch(() => []),
    fetchJson<Provider[]>('/api/providers/status').catch(() => []),
    fetchJson<any[]>('/api/alerts').catch(() => []),
    fetchJson<any[]>('/api/signals').catch(() => []),
  ])

  return <main className="space-y-4">
    <div className="flex items-center justify-between"><h1 className="text-2xl font-bold">WhaleScope</h1><span className="rounded bg-amber-700 px-2 py-1 text-xs">DEMO MODE</span></div>
    <AlertTicker />
    <section className="grid gap-3 md:grid-cols-4">
      <div className="card">Active alerts: {alerts.length}</div>
      <div className="card">Top bullish: {overview.sort((a,b)=>b.pressure-a.pressure)[0]?.symbol ?? 'n/a'}</div>
      <div className="card">Top bearish: {overview.sort((a,b)=>a.pressure-b.pressure)[0]?.symbol ?? 'n/a'}</div>
      <div className="card">Latest signals: {signals.length}</div>
    </section>
    <section className="card"><h2 className="mb-2 font-semibold">Provider health</h2><div className="flex gap-2">{providers.map((p)=><ProviderBadge key={p.provider} healthy={p.healthy} mode={p.mode}/> )}</div></section>
    <section className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
      {overview.map((o)=><Link className="card" href={`/assets/${o.symbol}`} key={o.symbol}><div className="font-semibold">{o.symbol}</div><div>{o.price.toFixed(4)}</div><div>24h {o.change_24h}%</div><div>Vol {Math.round(o.volume)}</div><div>Pressure {o.pressure.toFixed(1)}</div></Link>)}
    </section>
  </main>
}
