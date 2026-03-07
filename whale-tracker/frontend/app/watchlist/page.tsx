'use client'
import { useEffect, useState } from 'react'
import { API, apiGet } from '@/lib/api'

export default function WatchlistPage(){
  const [items,setItems] = useState<any[]>([])
  const [symbol,setSymbol] = useState('BTCUSDT')
  useEffect(()=>{apiGet('/api/watchlist').then(setItems)},[])
  const add = async()=>{
    await fetch(`${API}/api/watchlist`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({symbol,min_confidence:60,whale_threshold:200000,cooldown_seconds:120,enabled:true})})
    setItems(await apiGet('/api/watchlist'))
  }
  return <div className='space-y-3'><h1 className='text-xl font-bold'>Watchlist</h1>
    <div className='glass p-3 flex gap-2'><input value={symbol} onChange={e=>setSymbol(e.target.value)} className='bg-slate-800 px-2 py-1 rounded'/><button onClick={add} className='bg-cyan-700 px-3 py-1 rounded'>Add</button></div>
    {items.map(i=><div key={i.id} className='glass p-2'>{i.symbol} min confidence {i.min_confidence}</div>)}
  </div>
}
