import { fetchJson } from '@/lib/api'

export default async function SettingsPage() {
  const settings = await fetchJson<any>('/api/settings').catch(() => ({}))
  return <main className="space-y-3"><h1 className="text-xl">Admin Settings</h1><div className="card">Whale threshold: {settings.whale_threshold}</div><div className="card">Volume multiplier: {settings.volume_multiplier_threshold}</div><div className="card">Confidence cutoff: {settings.confidence_cutoff}</div><div className="card">Per-asset toggle is configurable via watchlist endpoint.</div><div className="card">Sound alert toggle available via notification config API model.</div></main>
}
