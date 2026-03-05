import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [alerts, setAlerts] = useState([])
  const [rules, setRules] = useState([])
  const [assets, setAssets] = useState([])
  const [health, setHealth] = useState({})
  const [form, setForm] = useState({ name: '', asset_type: 'crypto', symbol: '*', threshold_usd: 1000000, percent_move: 0, volume_multiple: 0, volatility_threshold: 0, cooldown_minutes: 15, key_levels: '' })

  const load = async () => {
    const [a, r, s, h] = await Promise.all([
      fetch(`${API}/alerts`).then(r => r.json()),
      fetch(`${API}/rules`).then(r => r.json()),
      fetch(`${API}/assets`).then(r => r.json()),
      fetch(`${API}/health`).then(r => r.json()),
    ])
    setAlerts(a); setRules(r); setAssets(s); setHealth(h)
  }

  useEffect(() => { load(); const i = setInterval(load, 10000); return () => clearInterval(i) }, [])

  const submitRule = async (e) => {
    e.preventDefault()
    const payload = { ...form, threshold_usd: Number(form.threshold_usd), percent_move: Number(form.percent_move), volume_multiple: Number(form.volume_multiple), volatility_threshold: Number(form.volatility_threshold), cooldown_minutes: Number(form.cooldown_minutes), key_levels: form.key_levels ? form.key_levels.split(',').map(Number) : [] }
    await fetch(`${API}/rules`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    await load()
  }

  return <div className="wrap">
    <h1>Whale Tracker & Cross-Asset Alerts</h1>
    <section><h2>Health</h2><pre>{JSON.stringify(health, null, 2)}</pre></section>
    <section><h2>Watchlist Assets</h2><ul>{assets.map(a => <li key={a.id}>{a.asset_type}: {a.symbol} @ {a.venue}</li>)}</ul></section>
    <section>
      <h2>Create Rule</h2>
      <form onSubmit={submitRule} className="grid">{Object.keys(form).map(k => <input key={k} value={form[k]} placeholder={k} onChange={e => setForm({ ...form, [k]: e.target.value })} />)}<button type="submit">Save Rule</button></form>
    </section>
    <section><h2>Rules</h2><ul>{rules.map(r => <li key={r.id}>{r.name} | {r.asset_type}/{r.symbol} | usd&gt;{r.threshold_usd}</li>)}</ul></section>
    <section><h2>Alerts Feed</h2><ul>{alerts.map(a => <li key={a.id}><b>{a.rule_name}</b> - {a.message}</li>)}</ul></section>
  </div>
}

createRoot(document.getElementById('root')).render(<App />)
