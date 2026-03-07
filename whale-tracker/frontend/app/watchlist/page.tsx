'use client'
import { useEffect, useState } from 'react'
import { fetchJson } from '@/lib/api'

export default function WatchlistPage() {
  const [list, setList] = useState<any[]>([])
  const [search, setSearch] = useState('')

  useEffect(() => { fetchJson<any[]>('/api/watchlist').then(setList).catch(() => {}) }, [])
  const filtered = list.filter((x) => x.symbol.toLowerCase().includes(search.toLowerCase()))

  return <main className="space-y-3"><h1 className="text-xl">Watchlist</h1><input className="rounded bg-slate-800 p-2" placeholder="search symbol" value={search} onChange={(e)=>setSearch(e.target.value)} />{filtered.map((w,i)=><div className="card" key={i}>{w.symbol} | threshold {w.whale_threshold} | min conf {w.min_confidence}</div>)}</main>
}
