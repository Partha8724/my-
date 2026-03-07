'use client'
export function FilterBar({timeframe,setTimeframe,search,setSearch}:{timeframe:string;setTimeframe:(v:string)=>void;search:string;setSearch:(v:string)=>void}) {
  return <div className='glass p-3 flex flex-wrap gap-2'>
    {['1m','5m','15m','1h'].map(tf => <button key={tf} className={`px-3 py-1 rounded ${timeframe===tf?'bg-cyan-600':'bg-slate-800'}`} onClick={()=>setTimeframe(tf)}>{tf}</button>)}
    <input className='bg-slate-800 rounded px-2 py-1 ml-auto' value={search} onChange={e=>setSearch(e.target.value)} placeholder='Search symbols' />
  </div>
}
