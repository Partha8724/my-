import { apiGet } from '@/lib/api'
import { AlertCard } from '@/components/alert-card'

export default async function AlertsPage(){
  const alerts = await apiGet('/api/alerts')
  return <div className='space-y-2'>{alerts.map((a:any)=><AlertCard key={a.id} alert={a} />)}</div>
}
