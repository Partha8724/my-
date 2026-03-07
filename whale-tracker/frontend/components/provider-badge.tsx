export function ProviderBadge({status,provider}:{status:string;provider:string}) {
  const tone = status === 'ok' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
  return <span className={`px-2 py-1 rounded text-xs ${tone}`}>{provider}: {status}</span>
}
