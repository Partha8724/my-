import { Signal } from '@/types'

export function SignalCard({signal,onOpen}:{signal:Signal;onOpen?:(s:Signal)=>void}) {
  const tone = signal.direction.includes('short') || signal.direction.includes('sell') ? 'text-rose-300' : 'text-cyan-300'
  return <button className='glass p-4 text-sm w-full text-left hover:border-cyan-500 transition' onClick={()=>onOpen?.(signal)}>
    <h3 className='font-semibold'>{signal.title} <span className={`text-xs ${tone}`}>({signal.direction})</span></h3>
    <p className='text-slate-300 mt-1'>{signal.why}</p>
    <p className='text-xs text-slate-400 mt-2'>Data source confidence: {signal.source_label}</p>
  </button>
}
