import { fetchJson } from '@/lib/api'

export default async function SignalsPage() {
  const signals = await fetchJson<any[]>('/api/signals').catch(() => [])
  return <main className="space-y-3"><h1 className="text-xl">Signals (informational)</h1>{signals.map((s,i)=><div className="card" key={i}><div className="font-semibold">{s.title} · {s.symbol}</div><div>{s.reason}</div><div className="text-sm">Entry: {s.entry_zone} | Inv: {s.invalidation} | T1: {s.target_1} | T2: {s.target_2}</div><div className="text-xs">Data source confidence: {s.data_source_confidence} · {s.source_label}</div></div>)}</main>
}
