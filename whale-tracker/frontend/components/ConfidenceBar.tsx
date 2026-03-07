export function ConfidenceBar({ score }: { score: number }) {
  return <div className="h-2 w-full rounded bg-slate-700"><div className="h-2 rounded bg-cyan-400" style={{ width: `${score}%` }} /></div>
}
