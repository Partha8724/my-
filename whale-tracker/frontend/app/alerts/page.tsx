import { fetchJson } from '@/lib/api'
import { ConfidenceBar } from '@/components/ConfidenceBar'

export default async function AlertsPage() {
  const alerts = await fetchJson<any[]>('/api/alerts').catch(() => [])
  return <main className="space-y-3"><h1 className="text-xl">Alerts</h1>{alerts.map((a,i)=><div className="card" key={i}><div>{a.symbol} · {a.direction} · {a.severity}</div><div>{a.reason}</div><ConfidenceBar score={a.confidence}/><div className="text-xs">source: {a.signal_source}</div></div>)}</main>
}
