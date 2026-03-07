import { apiGet } from '@/lib/api'

export default async function AssetPage({params}:{params:{symbol:string}}){
  const m = await apiGet(`/api/market/${params.symbol}`)
  const alerts = await apiGet('/api/alerts')
  const relevant = alerts.filter((a:any)=>a.asset===params.symbol).slice(0,10)
  return <div className='space-y-3'>
    <h1 className='text-2xl font-bold'>{params.symbol}</h1>
    <div className='glass p-3'>
      <p>Live price: {m.price?.toFixed?.(2)}</p>
      <p>Bullish vs bearish pressure: derived from latest signal direction.</p>
      <p className='text-xs text-slate-400'>Data source confidence label appears on each signal/alert card.</p>
    </div>
    <div className='glass p-3'>
      <h3 className='font-semibold'>Recent alerts</h3>
      {relevant.map((a:any)=><p key={a.id}>{a.timestamp} - {a.reason}</p>)}
    </div>
  </div>
}
