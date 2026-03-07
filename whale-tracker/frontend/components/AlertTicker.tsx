'use client'

import { useEffect, useState } from 'react'
import { API, fetchJson } from '@/lib/api'

type Alert = { symbol: string; reason: string; severity: string }

export function AlertTicker() {
  const [items, setItems] = useState<Alert[]>([])

  useEffect(() => {
    fetchJson<Alert[]>('/api/alerts').then((d) => setItems(d.slice(0, 10))).catch(() => {})
    const ws = new WebSocket(`${API.replace('http', 'ws')}/ws/stream`)
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data)
      if (msg.type === 'alert') setItems((prev) => [msg.payload, ...prev].slice(0, 10))
    }
    const ping = setInterval(() => ws.readyState === 1 && ws.send('ping'), 3000)
    return () => {
      clearInterval(ping)
      ws.close()
    }
  }, [])

  return <div className="overflow-hidden whitespace-nowrap rounded bg-slate-800 p-2 text-sm">{items.map((a, i) => <span className="mr-6" key={i}>🚨 {a.symbol} {a.severity}: {a.reason}</span>)}</div>
}
