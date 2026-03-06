import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })

function App() {
  const [alerts, setAlerts] = useState([])
  const [rules, setRules] = useState([])
  const [assets, setAssets] = useState([])
  const [health, setHealth] = useState({})
  const [events, setEvents] = useState([])
  const [metrics, setMetrics] = useState({ totals: {}, exposure: {}, assets: [], whale_wallets: [] })
  const [form, setForm] = useState({ name: '', asset_type: 'crypto', symbol: '*', threshold_usd: 1000000, percent_move: 0, volume_multiple: 0, volatility_threshold: 0, cooldown_minutes: 15, key_levels: '' })

  const load = async () => {
    const [a, r, s, h, e, m] = await Promise.all([
      fetch(`${API}/alerts`).then(r => r.json()),
      fetch(`${API}/rules`).then(r => r.json()),
      fetch(`${API}/assets`).then(r => r.json()),
      fetch(`${API}/health`).then(r => r.json()),
      fetch(`${API}/events?limit=80`).then(r => r.json()),
      fetch(`${API}/metrics/live?minutes=120`).then(r => r.json()),
    ])
    setAlerts(a); setRules(r); setAssets(s); setHealth(h); setEvents(e); setMetrics(m)
  }

  useEffect(() => { load(); const i = setInterval(load, 5000); return () => clearInterval(i) }, [])

  const submitRule = async (e) => {
    e.preventDefault()
    const payload = { ...form, threshold_usd: Number(form.threshold_usd), percent_move: Number(form.percent_move), volume_multiple: Number(form.volume_multiple), volatility_threshold: Number(form.volatility_threshold), cooldown_minutes: Number(form.cooldown_minutes), key_levels: form.key_levels ? form.key_levels.split(',').map(Number) : [] }
    await fetch(`${API}/rules`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    await load()
  }

  return <div className="wrap">
    <h1>Real-Time Crypto Whale Tracker</h1>
    <p className="muted">Tracks whale wallet flow, quantity, buy/sell + long/short pressure, and top assets by notional volume.</p>

    <section>
      <h2>Live Totals ({metrics.lookback_minutes || 0}m)</h2>
      <div className="kpis">
        <div className="card"><span>Events</span><strong>{metrics.totals.events || 0}</strong></div>
        <div className="card"><span>Total Volume</span><strong>{money.format(metrics.totals.total_volume_usd || 0)}</strong></div>
        <div className="card"><span>Buy Flow</span><strong>{money.format(metrics.totals.buy_volume_usd || 0)}</strong></div>
        <div className="card"><span>Sell Flow</span><strong>{money.format(metrics.totals.sell_volume_usd || 0)}</strong></div>
        <div className="card"><span>Long/Bullish Count</span><strong>{metrics.exposure.buy_count || 0}</strong></div>
        <div className="card"><span>Short/Bearish Count</span><strong>{metrics.exposure.sell_count || 0}</strong></div>
      </div>
    </section>

    <section><h2>Health</h2><pre>{JSON.stringify(health, null, 2)}</pre></section>
    <section><h2>Watchlist Assets</h2><ul>{assets.map(a => <li key={a.id}>{a.asset_type}: {a.symbol} @ {a.venue}</li>)}</ul></section>

    <section>
      <h2>Top Assets (Buy/Sell + Net)</h2>
      <table>
        <thead><tr><th>Asset</th><th>Type</th><th>Trades</th><th>Volume</th><th>Buy</th><th>Sell</th><th>Net</th></tr></thead>
        <tbody>
          {metrics.assets.map((item) => <tr key={`${item.asset}-${item.asset_type}`}>
            <td>{item.asset}</td>
            <td>{item.asset_type}</td>
            <td>{item.trade_count}</td>
            <td>{money.format(item.volume_usd)}</td>
            <td>{money.format(item.buy_usd)}</td>
            <td>{money.format(item.sell_usd)}</td>
            <td className={item.net_usd >= 0 ? 'green' : 'red'}>{money.format(item.net_usd)}</td>
          </tr>)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Whale Wallet Tracker</h2>
      <table>
        <thead><tr><th>Wallet</th><th>Activity</th><th>Volume</th><th>Last Seen</th></tr></thead>
        <tbody>
          {metrics.whale_wallets.map((w) => <tr key={w.wallet}><td>{w.wallet}</td><td>{w.activity_count}</td><td>{money.format(w.volume_usd)}</td><td>{w.last_seen || '-'}</td></tr>)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Real-Time Whale Tape</h2>
      <table>
        <thead><tr><th>Time</th><th>Asset</th><th>Type</th><th>Qty</th><th>USD</th><th>Side</th><th>From</th><th>To</th></tr></thead>
        <tbody>
          {events.map((event) => <tr key={event.id}>
            <td>{new Date(event.timestamp).toLocaleTimeString()}</td>
            <td>{event.asset_symbol}</td>
            <td>{event.event_type}</td>
            <td>{event.payload?.quantity || '-'}</td>
            <td>{money.format(event.amount_usd || 0)}</td>
            <td>{event.direction || event.payload?.side || '-'}</td>
            <td>{event.from_label || '-'}</td>
            <td>{event.to_label || '-'}</td>
          </tr>)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Create Rule</h2>
      <form onSubmit={submitRule} className="grid">{Object.keys(form).map(k => <input key={k} value={form[k]} placeholder={k} onChange={e => setForm({ ...form, [k]: e.target.value })} />)}<button type="submit">Save Rule</button></form>
    </section>
    <section><h2>Rules</h2><ul>{rules.map(r => <li key={r.id}>{r.name} | {r.asset_type}/{r.symbol} | usd&gt;{r.threshold_usd}</li>)}</ul></section>
    <section><h2>Alerts Feed</h2><ul>{alerts.map(a => <li key={a.id}><b>{a.rule_name}</b> - {a.message}</li>)}</ul></section>
  </div>
}

createRoot(document.getElementById('root')).render(<App />)
