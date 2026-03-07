'use client'
import { Signal } from '@/types'

export function SignalBreakdownModal({signal,onClose}:{signal:Signal|null;onClose:()=>void}) {
  if(!signal) return null
  return <div className='fixed inset-0 bg-black/60 z-40 flex items-center justify-center p-4' onClick={onClose}>
    <div className='glass p-5 w-full max-w-2xl space-y-3' onClick={e=>e.stopPropagation()}>
      <div className='flex justify-between items-center'><h3 className='text-xl font-bold'>{signal.title}</h3><button onClick={onClose}>✕</button></div>
      <p className='text-sm text-slate-300'>{signal.why}</p>
      <div className='grid grid-cols-2 gap-2 text-sm'>
        <div className='glass p-2'>Entry: {signal.entry_zone}</div>
        <div className='glass p-2'>Invalidation: {signal.invalidation}</div>
        <div className='glass p-2'>Target 1: {signal.target1}</div>
        <div className='glass p-2'>Target 2: {signal.target2}</div>
      </div>
      <div className='text-xs text-cyan-300'>Data source confidence: {signal.source_label}</div>
      {signal.analytics && <div className='grid grid-cols-2 gap-2 text-xs text-slate-300'>
        <p>Imbalance: {(signal.analytics.buy_sell_imbalance*100).toFixed(1)}%</p>
        <p>Cumulative Delta: {Math.round(signal.analytics.cumulative_delta)}</p>
        <p>Volatility: {(signal.analytics.volatility*10000).toFixed(2)} bp</p>
        <p>Regime: {signal.analytics.trend_regime}</p>
      </div>}
    </div>
  </div>
}
