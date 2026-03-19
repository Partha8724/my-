import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const defaultForm = {
  name: '',
  asset_type: 'crypto',
  symbol: '*',
  threshold_usd: 1000000,
  percent_move: 0,
  volume_multiple: 0,
  volatility_threshold: 0,
  cooldown_minutes: 15,
  key_levels: '',
}

const clamp = (value, min, max) => Math.min(max, Math.max(min, value))

const compactNumber = (value) => {
  if (!value) return '$0'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value)
}

const formatDate = (value) => {
  if (!value) return 'No update'
  return new Date(value).toLocaleString()
}

const formatPrice = (value) => {
  if (value == null) return 'Live price unavailable'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: value >= 1000 ? 2 : 4,
  }).format(value)
}

const formatPercent = (value) => {
  if (value == null) return 'n/a'
  const rounded = value.toFixed(2)
  return `${value >= 0 ? '+' : ''}${rounded}%`
}

const Sparkline = ({ points = [] }) => {
  if (!points.length) return null
  const width = 120
  const height = 44
  const min = Math.min(...points)
  const max = Math.max(...points)
  const span = max - min || 1
  const polyline = points
    .map((point, index) => {
      const x = (index / Math.max(points.length - 1, 1)) * width
      const y = height - ((point - min) / span) * (height - 6) - 3
      return `${x},${y}`
    })
    .join(' ')

  return (
    <svg className="sparkline" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
      <polyline fill="none" stroke="currentColor" strokeWidth="3" points={polyline} />
    </svg>
  )
}

const parseAlert = (alert) => {
  const base = {
    ...alert,
    symbol: 'UNKNOWN',
    eventType: 'unknown',
    sizeUsd: 0,
    source: 'unknown',
    reason: '',
    bias: 'neutral',
    confidenceBoost: 0,
  }

  const symbolMatch = alert.message.match(/^([A-Z0-9]+)/)
  const eventTypeMatch = alert.message.match(/^[A-Z0-9]+\s+([a-z_]+)/)
  const sizeMatch = alert.message.match(/size=\$([\d,]+)/)
  const sourceMatch = alert.message.match(/source=([a-z0-9-]+)/i)
  const reasonMatch = alert.message.match(/why=(.*)$/i)

  base.symbol = symbolMatch?.[1] || base.symbol
  base.eventType = eventTypeMatch?.[1] || base.eventType
  base.sizeUsd = Number((sizeMatch?.[1] || '0').replaceAll(',', ''))
  base.source = sourceMatch?.[1] || base.source
  base.reason = reasonMatch?.[1] || ''

  if (base.eventType === 'large_swap') {
    base.bias = 'bullish'
    base.confidenceBoost += 16
  } else if (base.eventType === 'exchange_flow') {
    base.bias = 'bearish'
    base.confidenceBoost -= 12
  } else if (base.eventType === 'large_transfer') {
    base.bias = 'bullish'
    base.confidenceBoost += 8
  } else if (base.eventType === 'price_spike') {
    base.bias = 'bullish'
    base.confidenceBoost += 10
  } else if (base.eventType === 'unusual_volume') {
    base.bias = 'neutral'
    base.confidenceBoost += 4
  }

  if (base.rule_name?.includes('xau') || base.rule_name?.includes('stock')) {
    base.confidenceBoost -= 2
  }

  if (base.sizeUsd >= 5000000) base.confidenceBoost += 14
  else if (base.sizeUsd >= 1000000) base.confidenceBoost += 8
  else if (base.sizeUsd > 0) base.confidenceBoost += 4

  return base
}

const buildCoinSignals = (assets, alerts, rules) => {
  const cryptoAssets = assets.filter((asset) => asset.asset_type === 'crypto')
  const ruleIndex = rules.reduce((acc, rule) => {
    acc[`${rule.asset_type}:${rule.symbol}`] = rule
    return acc
  }, {})

  const symbols = new Set([
    ...cryptoAssets.map((asset) => asset.symbol),
    ...alerts.map((alert) => alert.symbol).filter(Boolean),
  ])

  return [...symbols]
    .map((symbol) => {
      const asset = cryptoAssets.find((item) => item.symbol === symbol)
      const coinAlerts = alerts.filter((item) => item.symbol === symbol)
      const totalWhaleUsd = coinAlerts.reduce((sum, item) => sum + item.sizeUsd, 0)
      const rawScore = coinAlerts.reduce((sum, item) => sum + item.confidenceBoost, 50)
      const score = clamp(rawScore, 8, 92)
      const bullishChance = clamp(Math.round(score), 1, 99)
      const bearishChance = 100 - bullishChance
      const latest = coinAlerts[0]
      const dominantBias =
        bullishChance >= 60 ? 'LONG' : bearishChance >= 60 ? 'SHORT' : 'WAIT'
      const triggerRule =
        ruleIndex[`crypto:${symbol}`] ||
        ruleIndex['crypto:*'] ||
        null

      return {
        symbol,
        venue: asset?.venue || latest?.source || 'tracked',
        bullishChance,
        bearishChance,
        dominantBias,
        totalWhaleUsd,
        alertCount: coinAlerts.length,
        latestEvent: latest?.eventType || 'No fresh whale event',
        sourceCount: 1,
        summary:
          latest?.bias === 'bearish'
            ? 'Exchange-facing whale pressure is elevated.'
            : latest?.bias === 'bullish'
              ? 'Recent whale flow supports upside continuation.'
              : 'No directional edge from the current whale tape.',
        threshold: triggerRule?.threshold_usd || 0,
      }
    })
    .sort((a, b) => b.bullishChance - a.bullishChance)
}

function App() {
  const [alerts, setAlerts] = useState([])
  const [rules, setRules] = useState([])
  const [assets, setAssets] = useState([])
  const [signals, setSignals] = useState([])
  const [whaleOrders, setWhaleOrders] = useState([])
  const [assistantBrief, setAssistantBrief] = useState(null)
  const [health, setHealth] = useState({})
  const [form, setForm] = useState(defaultForm)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [view, setView] = useState('all')
  const [selectedSymbol, setSelectedSymbol] = useState('ALL')

  const load = async () => {
    try {
      setError('')
      const [a, r, s, h] = await Promise.all([
        fetch(`${API}/alerts`).then((response) => response.json()),
        fetch(`${API}/rules`).then((response) => response.json()),
        fetch(`${API}/assets`).then((response) => response.json()),
        fetch(`${API}/health`).then((response) => response.json()),
      ])
      const [signalResponse, whaleOrderResponse, assistantResponse] = await Promise.all([
        fetch(`${API}/signals`),
        fetch(`${API}/whale-orders?limit=40`),
        fetch(`${API}/assistant`),
      ])
      const liveSignals = signalResponse.ok ? await signalResponse.json() : []
      const liveWhaleOrders = whaleOrderResponse.ok ? await whaleOrderResponse.json() : []
      const liveAssistant = assistantResponse.ok ? await assistantResponse.json() : null
      setAlerts(a)
      setRules(r)
      setAssets(s)
      setSignals(liveSignals)
      setWhaleOrders(liveWhaleOrders)
      setAssistantBrief(liveAssistant)
      setHealth(h)
    } catch (err) {
      setError('API offline. Start the backend to load live whale and signal data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    const interval = setInterval(load, 10000)
    return () => clearInterval(interval)
  }, [])

  const submitRule = async (event) => {
    event.preventDefault()
    const payload = {
      ...form,
      threshold_usd: Number(form.threshold_usd),
      percent_move: Number(form.percent_move),
      volume_multiple: Number(form.volume_multiple),
      volatility_threshold: Number(form.volatility_threshold),
      cooldown_minutes: Number(form.cooldown_minutes),
      key_levels: form.key_levels
        ? form.key_levels.split(',').map((item) => Number(item.trim())).filter(Boolean)
        : [],
    }

    await fetch(`${API}/rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    setForm(defaultForm)
    await load()
  }

  const parsedAlerts = useMemo(() => alerts.map(parseAlert), [alerts])
  const fallbackSignals = useMemo(
    () => buildCoinSignals(assets, parsedAlerts, rules),
    [assets, parsedAlerts, rules],
  )
  const cryptoSignals = useMemo(
    () =>
      signals.length
        ? signals.map((item) => ({
            symbol: item.symbol,
            venue: item.venue,
            bullishChance: item.bullish_chance,
            bearishChance: item.bearish_chance,
            dominantBias: item.signal,
            totalWhaleUsd: item.total_whale_usd,
            alertCount: item.alert_count,
            latestEvent: item.last_event_type,
            summary: item.summary,
            whaleDirection: item.whale_direction,
            sources: item.sources,
            sourceCount: item.sources?.length || 0,
            updatedAt: item.last_event_at,
            trend: item.trend,
          }))
        : fallbackSignals,
    [fallbackSignals, signals],
  )
  const symbolOptions = useMemo(
    () => ['ALL', ...new Set(cryptoSignals.map((item) => item.symbol))],
    [cryptoSignals],
  )
  const filteredSignals = useMemo(() => {
    const symbolScoped =
      selectedSymbol === 'ALL'
        ? cryptoSignals
        : cryptoSignals.filter((item) => item.symbol === selectedSymbol)

    if (view === 'bullish') {
      return symbolScoped.filter((item) => item.dominantBias === 'LONG').sort((a, b) => b.bullishChance - a.bullishChance)
    }
    if (view === 'bearish') {
      return symbolScoped.filter((item) => item.dominantBias === 'SHORT').sort((a, b) => b.bearishChance - a.bearishChance)
    }
    return symbolScoped
  }, [cryptoSignals, selectedSymbol, view])
  const leader = filteredSignals[0] || cryptoSignals[0]
  const shortLeader = [...cryptoSignals].sort((a, b) => b.bearishChance - a.bearishChance)[0]
  const assistantWatchlist = (assistantBrief?.watchlist || []).filter((item) => item.signal !== 'SHORT')
  const assistantLeader = assistantBrief?.best_setup || leader
  const assistantShort = assistantBrief?.best_short || shortLeader
  const whaleTape = useMemo(() => {
    const scopedOrders =
      selectedSymbol === 'ALL'
        ? whaleOrders
        : whaleOrders.filter((item) => item.symbol === selectedSymbol)
    return scopedOrders.slice(0, 8)
  }, [selectedSymbol, whaleOrders])

  return (
    <div className="app-shell">
      <div className="backdrop backdrop-left" />
      <div className="backdrop backdrop-right" />

      <main className="dashboard">
        <section className="hero panel">
          <div>
            <p className="eyebrow">AI Trading Assistant</p>
            <h1>Live crypto market read, ranked setups, and a forward-looking bullish watchlist.</h1>
            <p className="lede">
              This assistant combines whale events with live market data when available, then ranks
              which coin has the cleanest setup. It is a decision-support tool, not financial advice.
            </p>
          </div>

          <div className="hero-metrics">
            <article className="metric-card">
              <span>Best long setup</span>
              <strong>{assistantLeader ? assistantLeader.symbol : '--'}</strong>
              <p>
                {assistantLeader
                  ? `${assistantLeader.bullishChance}% bullish, ${assistantLeader.outlook || assistantLeader.summary}`
                  : 'Waiting for crypto alerts'}
              </p>
            </article>
            <article className="metric-card">
              <span>Top short setup</span>
              <strong>{assistantShort ? assistantShort.symbol : '--'}</strong>
              <p>
                {assistantShort
                  ? `${assistantShort.bearishChance}% bearish chance`
                  : 'Waiting for crypto alerts'}
              </p>
            </article>
            <article className="metric-card">
              <span>Market mode</span>
              <strong>{assistantBrief?.market_mode || (loading ? 'Loading' : 'Fallback')}</strong>
              <p>Last refresh: {health.last_run || 'pending'}</p>
            </article>
          </div>
        </section>

        {error ? <section className="panel banner error">{error}</section> : null}

        <section className="content-grid">
          <article className="panel">
            <div className="panel-title-row">
              <div>
                <p className="eyebrow">Assistant Read</p>
                <h2>What looks strongest right now</h2>
              </div>
            </div>
            <div className="narrative">
              {(assistantBrief?.commentary || []).map((item) => (
                <div className="narrative-card" key={item}>
                  <span>Assistant insight</span>
                  <p>{item}</p>
                </div>
              ))}
              {!assistantBrief?.commentary?.length ? (
                <div className="narrative-card">
                  <span>Assistant insight</span>
                  <p>Waiting for enough market and whale data to form a read.</p>
                </div>
              ) : null}
            </div>
          </article>

          <article className="panel">
            <div className="panel-title-row">
              <div>
                <p className="eyebrow">Future Bullish Watch</p>
                <h2>Coins with improving structure</h2>
              </div>
            </div>
            <div className="watchlist">
              {assistantWatchlist.length ? (
                assistantWatchlist.slice(0, 4).map((coin) => (
                  <div className="watch-item" key={coin.symbol}>
                    <div className="watch-top">
                      <strong>{coin.symbol}</strong>
                      <span className={`bias-pill ${coin.signal.toLowerCase()}`}>{coin.outlook}</span>
                    </div>
                    <p>{coin.summary}</p>
                    <div className="watch-stats">
                      <span>{formatPrice(coin.price)}</span>
                      <span className={coin.change_24h >= 0 ? 'positive' : 'negative'}>
                        {formatPercent(coin.change_24h)}
                      </span>
                      <span>Quality {coin.setup_quality}%</span>
                    </div>
                  </div>
                ))
              ) : (
                <p className="empty-copy">No bullish watchlist yet.</p>
              )}
            </div>
          </article>
        </section>

        <section className="panel section-head">
          <div>
            <p className="eyebrow">Signal Board</p>
            <h2>High-quality setups ranked by whale flow and live tape</h2>
          </div>
          <div className="signal-controls">
            <div className="control-group">
              <button className={view === 'all' ? 'active' : ''} onClick={() => setView('all')} type="button">
                All
              </button>
              <button className={view === 'bullish' ? 'active' : ''} onClick={() => setView('bullish')} type="button">
                Top bullish
              </button>
              <button className={view === 'bearish' ? 'active' : ''} onClick={() => setView('bearish')} type="button">
                Top bearish
              </button>
            </div>
            <select value={selectedSymbol} onChange={(event) => setSelectedSymbol(event.target.value)}>
              {symbolOptions.map((symbol) => (
                <option key={symbol} value={symbol}>
                  {symbol === 'ALL' ? 'All coins' : symbol}
                </option>
              ))}
            </select>
          </div>
        </section>

        <section className="signals-grid">
          {filteredSignals.length ? (
            filteredSignals.map((coin) => (
              <article className="signal-card panel" key={coin.symbol}>
                <div className="signal-top">
                  <div>
                    <p className="coin-symbol">{coin.symbol}</p>
                    <p className="coin-venue">{coin.venue}</p>
                  </div>
                  <span className={`bias-pill ${coin.dominantBias.toLowerCase()}`}>{coin.dominantBias}</span>
                </div>

                <div className="probability">
                  <div>
                    <span>Bullish</span>
                    <strong>{coin.bullishChance}%</strong>
                  </div>
                  <div>
                    <span>Bearish</span>
                    <strong>{coin.bearishChance}%</strong>
                  </div>
                </div>

                <div className="meter">
                  <div className="meter-bull" style={{ width: `${coin.bullishChance}%` }} />
                </div>

                {coin.trend?.length ? (
                  <div className={`chart-wrap ${coin.dominantBias.toLowerCase()}`}>
                    <Sparkline points={coin.trend} />
                    <span>6h whale trend</span>
                  </div>
                ) : null}

                <dl className="signal-stats">
                  <div>
                    <dt>Whale size</dt>
                    <dd>{compactNumber(coin.totalWhaleUsd)}</dd>
                  </div>
                  <div>
                    <dt>Alert count</dt>
                    <dd>{coin.alertCount}</dd>
                  </div>
                  <div>
                    <dt>Sources</dt>
                    <dd>{coin.sourceCount || coin.sources?.length || 0}</dd>
                  </div>
                  <div>
                    <dt>Latest event</dt>
                    <dd>{coin.latestEvent}</dd>
                  </div>
                </dl>

                <p className="signal-summary">{coin.summary}</p>
                {coin.whaleDirection ? (
                  <p className="section-note">Whale flow: {coin.whaleDirection}</p>
                ) : null}
              </article>
            ))
          ) : (
            <article className="signal-card panel empty-card">
              <p>No signals match this filter.</p>
              <span>Switch the coin or bias filter, or wait for new whale activity.</span>
            </article>
          )}
        </section>

        <section className="content-grid">
          <article className="panel">
            <div className="panel-title-row">
              <div>
                <p className="eyebrow">Whale Tape</p>
                <h2>Recent whale orders</h2>
              </div>
            </div>

            <div className="tape-list">
              {whaleTape.length ? (
                whaleTape.map((item) => (
                  <div className="tape-item" key={item.event_uid}>
                    <div>
                      <strong>{item.symbol}</strong>
                      <span>{item.event_type.replaceAll('_', ' ')}</span>
                    </div>
                    <div>
                      <strong>{compactNumber(item.amount_usd)}</strong>
                      <span className={`tape-bias ${item.bias}`}>{item.bias}</span>
                    </div>
                    <time>{formatDate(item.timestamp)}</time>
                  </div>
                ))
              ) : (
                <p className="empty-copy">No whale orders yet.</p>
              )}
            </div>
          </article>

          <article className="panel">
            <p className="eyebrow">Live Engine</p>
            <h2>Live market read</h2>
            <div className="narrative">
              <div className="narrative-card">
                <span>Best bullish candidate</span>
                <strong>{assistantLeader ? assistantLeader.symbol : '--'}</strong>
                <p>{assistantLeader ? assistantLeader.summary : 'No active whale-led crypto setup yet.'}</p>
              </div>
              <div className="narrative-card">
                <span>Best bearish candidate</span>
                <strong>{assistantShort ? assistantShort.symbol : '--'}</strong>
                <p>
                  {assistantShort
                    ? `${assistantShort.bearishChance}% bearish chance based on recent pressure.`
                    : 'No active bearish leader yet.'}
                </p>
              </div>
              <div className="narrative-card">
                <span>Live data coverage</span>
                <strong>
                  {assistantWatchlist.filter((item) => item.live_supported).length}/{assistantWatchlist.length || 0}
                </strong>
                <p>{rules.length} active rules and {whaleOrders.length} recent whale orders in the tape.</p>
              </div>
            </div>
          </article>
        </section>

        <section className="content-grid lower">
          <article className="panel">
            <p className="eyebrow">Rule Builder</p>
            <h2>Create a custom signal rule</h2>
            <form onSubmit={submitRule} className="rule-form">
              <label>
                Rule name
                <input
                  value={form.name}
                  placeholder="btc_whale_breakout"
                  onChange={(event) => setForm({ ...form, name: event.target.value })}
                />
              </label>
              <label>
                Asset type
                <select
                  value={form.asset_type}
                  onChange={(event) => setForm({ ...form, asset_type: event.target.value })}
                >
                  <option value="crypto">Crypto</option>
                  <option value="stock">Stock</option>
                  <option value="metal">Metal</option>
                  <option value="any">Any</option>
                </select>
              </label>
              <label>
                Symbol
                <input
                  value={form.symbol}
                  placeholder="BTC"
                  onChange={(event) => setForm({ ...form, symbol: event.target.value.toUpperCase() })}
                />
              </label>
              <label>
                Whale threshold USD
                <input
                  type="number"
                  value={form.threshold_usd}
                  onChange={(event) => setForm({ ...form, threshold_usd: event.target.value })}
                />
              </label>
              <label>
                Percent move
                <input
                  type="number"
                  step="0.1"
                  value={form.percent_move}
                  onChange={(event) => setForm({ ...form, percent_move: event.target.value })}
                />
              </label>
              <label>
                Volume multiple
                <input
                  type="number"
                  step="0.1"
                  value={form.volume_multiple}
                  onChange={(event) => setForm({ ...form, volume_multiple: event.target.value })}
                />
              </label>
              <label>
                Volatility threshold
                <input
                  type="number"
                  step="0.1"
                  value={form.volatility_threshold}
                  onChange={(event) => setForm({ ...form, volatility_threshold: event.target.value })}
                />
              </label>
              <label>
                Cooldown minutes
                <input
                  type="number"
                  value={form.cooldown_minutes}
                  onChange={(event) => setForm({ ...form, cooldown_minutes: event.target.value })}
                />
              </label>
              <label className="full-span">
                Key levels
                <input
                  value={form.key_levels}
                  placeholder="95000, 100000"
                  onChange={(event) => setForm({ ...form, key_levels: event.target.value })}
                />
              </label>
              <button type="submit">Save signal rule</button>
            </form>
          </article>

          <article className="panel">
            <p className="eyebrow">Alert Feed</p>
            <h2>Latest signals</h2>
            <div className="alerts-list">
              {parsedAlerts.slice(0, 6).map((item) => (
                <div className="alert-item" key={item.id}>
                  <div className="alert-row">
                    <strong>{item.symbol}</strong>
                    <span>{item.rule_name}</span>
                  </div>
                  <p>{item.message}</p>
                  <div className="alert-row muted">
                    <span>{compactNumber(item.sizeUsd)}</span>
                    <span>{formatDate(item.created_at)}</span>
                  </div>
                </div>
              ))}
              {!parsedAlerts.length ? <p className="empty-copy">No alerts stored yet.</p> : null}
            </div>
          </article>
        </section>
      </main>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
