import { apiGet } from '@/lib/api'
import { SignalCard } from '@/components/signal-card'

export default async function SignalsPage(){
  const signals = await apiGet('/api/signals')
  return <div className='space-y-2'>{signals.map((s:any)=><SignalCard key={s.id} signal={s} />)}</div>
}
