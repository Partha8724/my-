export function ConfidenceBar({value}:{value:number}) {
  const c = value > 80 ? 'bg-emerald-400' : value > 60 ? 'bg-cyan-400' : 'bg-amber-400'
  return <div className='w-full h-2 bg-slate-800 rounded'>
    <div className={`h-2 rounded ${c}`} style={{width:`${value}%`}} />
  </div>
}
