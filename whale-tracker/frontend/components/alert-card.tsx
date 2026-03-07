import { Alert } from '@/types'
import { ConfidenceBar } from './confidence-bar'

export function AlertCard({alert}:{alert:Alert}) {
  const tone = alert.direction.includes('sell') || alert.direction.includes('short') ? 'text-rose-300' : 'text-emerald-300'
  return <div className='glass p-4 space-y-2'>
    <div className='flex justify-between items-center'><b>{alert.asset}</b><span className={`text-xs ${tone}`}>{alert.direction}</span></div>
    <p className='text-sm text-slate-200'>{alert.reason}</p>
    <div className='flex justify-between text-xs text-slate-400'><span>source: {alert.source_label}</span><span>{alert.severity}</span></div>
    <ConfidenceBar value={alert.confidence} />
  </div>
}
