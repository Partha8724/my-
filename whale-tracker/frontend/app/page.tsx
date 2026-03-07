'use client'
import Link from 'next/link'
import { useEffect, useMemo, useState } from 'react'
import { AlertCard } from '@/components/alert-card'
import { FilterBar } from '@/components/filter-bar'
import { LiveTicker } from '@/components/live-ticker'
import { ProviderBadge } from '@/components/provider-badge'
import { SignalCard } from '@/components/signal-card'
import { SignalBreakdownModal } from '@/components/signal-breakdown-modal'
import { API, apiGet } from '@/lib/api'
import { Alert, Signal } from '@/types'

function HeatCell({symbol,score,regime}:{symbol:string;score:number;regime:string}){
  const bg = score > 15 ? 'bg-emerald-500/20 border-emerald-500/50' : score < -15 ? 'bg-rose-500/20 border-rose-500/50' : 'bg-slate-800/80 border-slate-700'
  return <div className={`p-2 rounded-xl border ${bg}`}><p className='font-semibold text-sm'>{symbol}</p><p className='text-xs'>{score.toFixed(1)} | {regime}</p></div>
}

export default function DashboardPage(){
  const [overview,setOverview] = useState<any>(null)
  const [alerts,setAlerts] = useState<Alert[]>([])
  const [signals,setSignals] = useState<Signal[]>([])
  const [timeframe,setTimeframe] = useState('1m')
  const [search,setSearch] = useState('')
  const [sound, setSound] = useState(false)
  const [selected, setSelected] = useState<Signal | null>(null)

  useEffect(()=>{const load=async()=>{setOverview(await apiGet('/api/market/overview'));setAlerts(await apiGet('/api/alerts'));setSignals(await apiGet('/api/signals'))};load();const id=setInterval(load,4000);return ()=>clearInterval(id)},[])

  useEffect(()=>{
    const ws = new WebSocket(API.replace('http','ws') + '/ws/stream')
    ws.onmessage = (e)=>{ const data = JSON.parse(e.data); if(data.type==='alert'){ setAlerts(v=>[data.payload,...v].slice(0,200)); if(sound) new Audio('/ping.mp3').play().catch(()=>{}) } if(data.type==='signal') setSignals(v=>[data.payload,...v].slice(0,200)); if(data.type==='ticker'){ setOverview((prev:any)=> prev ? {...prev, market: {...prev.market, [data.payload.symbol]: data.payload}} : prev) } }
    ws.onopen = ()=>ws.send('hello')
    return ()=>ws.close()
  },[sound])

  const filtered = useMemo(()=>alerts.filter(a=>a.asset.toLowerCase().includes(search.toLowerCase())),[alerts,search])
  const marketList = Object.values(overview?.market || {}).filter((m:any)=> String(m.symbol).toLowerCase().includes(search.toLowerCase())) as any[]

  return <div className='space-y-5'>
    <section className='glass p-8 bg-gradient-to-r from-indigo-950/90 via-slate-900 to-cyan-950/60'>
      <h1 className='text-4xl md:text-5xl font-black tracking-tight'>WhaleScope Command Center</h1>
      <p className='text-slate-300 mt-2'>Live whale activity intelligence for Crypto, XAUUSD, and XAGUSD.</p>
      <div className='mt-4 flex gap-2 text-xs'><span className='px-2 py-1 bg-red-500/20 rounded'>informational signals only</span><span className='px-2 py-1 bg-cyan-500/20 rounded'>timeframe {timeframe}</span></div>
    </section>

    <FilterBar timeframe={timeframe} setTimeframe={setTimeframe} search={search} setSearch={setSearch} />
    <LiveTicker alerts={alerts} />

    <section className='grid xl:grid-cols-4 gap-3'>
      <div className='glass p-4'><p className='panel-title'>Active Alerts</p><p className='text-2xl font-bold'>{overview?.total_active_alerts || 0}</p></div>
      <div className='glass p-4'><p className='panel-title'>Top Bullish</p><p className='text-2xl font-bold text-emerald-300'>{overview?.top_movers?.[0]?.symbol || '-'}</p></div>
      <div className='glass p-4'><p className='panel-title'>Top Bearish</p><p className='text-2xl font-bold text-rose-300'>{overview?.top_movers?.[1]?.symbol || '-'}</p></div>
      <div className='glass p-4'><p className='panel-title'>Connection</p><div className='flex flex-wrap gap-1 mt-1'>{(overview?.provider_status || []).map((p:any)=><ProviderBadge key={p.provider} provider={p.provider} status={p.status} />)}</div></div>
    </section>

    <div className='flex gap-2 items-center'>
      <label className='text-sm'><input type='checkbox' checked={sound} onChange={e=>setSound(e.target.checked)} /> sound alert</label>
      <a href={`${API}/api/alerts/export.csv`} className='text-sm underline text-cyan-300'>Export Alerts CSV</a>
    </div>

    <section className='grid xl:grid-cols-3 gap-3'>
      <div className='glass p-4 xl:col-span-2'>
        <p className='panel-title mb-2'>Tracked Assets</p>
        <div className='grid md:grid-cols-3 gap-3'>
          {marketList.map((m:any)=><Link className='glass p-3 hover:border-cyan-500 transition' key={m.symbol} href={`/asset/${m.symbol}`}><h3 className='font-semibold'>{m.symbol}</h3><p className='text-xl font-bold'>{m.price?.toFixed?.(2)}</p><p className='text-xs text-slate-400'>volume {Math.round(m.volume||0)}</p><p className='text-xs'>imbalance {((m.analytics?.buy_sell_imbalance||0)*100).toFixed(1)}%</p></Link>)}
        </div>
      </div>
      <div className='glass p-4'>
        <p className='panel-title mb-2'>Top Movers</p>
        <div className='space-y-2'>{(overview?.top_movers || []).map((m:any)=><div key={m.symbol} className='glass p-2'><p className='font-semibold'>{m.symbol}</p><p className='text-xs text-slate-300'>delta {Math.round(m.analytics?.cumulative_delta || 0)} | regime {m.analytics?.trend_regime}</p></div>)}</div>
      </div>
    </section>

    <section className='glass p-4'>
      <p className='panel-title mb-2'>Heatmap</p>
      <div className='grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2'>
        {(overview?.heatmap || []).map((h:any)=><HeatCell key={h.symbol} symbol={h.symbol} score={h.score} regime={h.regime} />)}
      </div>
    </section>

    <section className='grid lg:grid-cols-2 gap-3'>
      <div className='space-y-2'><p className='panel-title'>Latest Alerts</p>{filtered.slice(0,8).map(a=><AlertCard key={a.id+''+a.timestamp} alert={a} />)}</div>
      <div className='space-y-2'><p className='panel-title'>Signals</p>{signals.slice(0,8).map(s=><SignalCard key={s.id+''+s.timestamp} signal={s} onOpen={setSelected} />)}</div>
    </section>

    <SignalBreakdownModal signal={selected} onClose={()=>setSelected(null)} />
  </div>
}
