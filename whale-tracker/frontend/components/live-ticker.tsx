'use client'
import { Alert } from '@/types'

export function LiveTicker({alerts}:{alerts:Alert[]}) {
  return <div className='glass p-2 overflow-hidden'>
    <div className='whitespace-nowrap animate-[scroll_25s_linear_infinite]'>
      {alerts.slice(0,10).map(a => <span className='mr-8 text-sm' key={a.id}>{a.asset} {a.direction} {a.confidence}%</span>)}
    </div>
    <style jsx>{`@keyframes scroll{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}`}</style>
  </div>
}
