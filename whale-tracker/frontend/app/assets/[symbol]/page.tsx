import { fetchJson } from '@/lib/api'

export default async function AssetPage({ params }: { params: { symbol: string } }) {
  const [market, history, alerts] = await Promise.all([
    fetchJson<any>(`/api/market/${params.symbol}`).catch(() => ({})),
    fetchJson<any>(`/api/market/${params.symbol}/history?timeframe=5m`).catch(() => ({ events: [] })),
    fetchJson<any[]>('/api/alerts').catch(() => []),
  ])
  return <main className="space-y-3"><h1 className="text-xl">{params.symbol} Detail</h1><div className="card">Live price: {market.price}</div><div className="card">Bullish/Bearish pressure: {market.pressure}</div><div className="card">Timeframe filters: 1m / 5m / 15m / 1h</div><div className="card">Recent events: {history.events.slice(0,8).map((e:any,i:number)=><div key={i}>{e.side} {Math.round(e.size)} @ {e.price}</div>)}</div><div className="card">Related alerts: {alerts.filter(a=>a.symbol===params.symbol).slice(0,5).map((a,i)=><div key={i}>{a.reason}</div>)}</div><div className="card">Explanation panel: Signals are informational alerts and include source labels (confirmed flow, derived proxy, futures tape proxy, volume spike proxy, mock/demo data).</div></main>
}
