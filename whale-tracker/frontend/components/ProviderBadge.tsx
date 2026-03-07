export function ProviderBadge({ healthy, mode }: { healthy: boolean; mode: string }) {
  return <span className={`rounded px-2 py-1 text-xs ${healthy ? 'bg-emerald-700' : 'bg-red-700'}`}>{healthy ? 'healthy' : 'down'} · {mode}</span>
}
