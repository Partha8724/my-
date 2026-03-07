'use client'

import { useEffect, useState } from 'react'

import { apiGet, apiPut } from '@/lib/api'

type SettingsPayload = {
  whale_trade_threshold_usd:number
  volume_multiplier_threshold:number
  confidence_cutoff:number
  symbol_cooldown_seconds:number
  duplicate_suppression_seconds:number
  confirmation_window_seconds:number
  confirmation_hits:number
  asset_enabled: Record<string, boolean>
}

export default function SettingsPage(){
  const [form,setForm] = useState<SettingsPayload | null>(null)
  const [status,setStatus] = useState('')

  useEffect(()=>{
    apiGet('/api/settings').then((v)=>setForm(v))
  },[])

  const save = async() => {
    if(!form) return
    await apiPut('/api/settings', form)
    setStatus('Saved')
    setTimeout(()=>setStatus(''), 1500)
  }

  if(!form) return <div className='glass p-4'>Loading settings...</div>

  return <div className='space-y-3'>
    <h1 className='text-xl font-bold'>Admin Settings</h1>
    <div className='glass p-4 grid md:grid-cols-3 gap-3'>
      <label>Whale size threshold<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.whale_trade_threshold_usd} onChange={e=>setForm({...form, whale_trade_threshold_usd:Number(e.target.value)})}/></label>
      <label>Volume multiplier<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.volume_multiplier_threshold} onChange={e=>setForm({...form, volume_multiplier_threshold:Number(e.target.value)})}/></label>
      <label>Confidence cutoff<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.confidence_cutoff} onChange={e=>setForm({...form, confidence_cutoff:Number(e.target.value)})}/></label>
      <label>Symbol cooldown (s)<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.symbol_cooldown_seconds} onChange={e=>setForm({...form, symbol_cooldown_seconds:Number(e.target.value)})}/></label>
      <label>Duplicate suppression (s)<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.duplicate_suppression_seconds} onChange={e=>setForm({...form, duplicate_suppression_seconds:Number(e.target.value)})}/></label>
      <label>Confirmation hits<input type='number' className='block w-full bg-slate-800 rounded p-1' value={form.confirmation_hits} onChange={e=>setForm({...form, confirmation_hits:Number(e.target.value)})}/></label>
    </div>

    <div className='glass p-4'>
      <h2 className='font-semibold mb-2'>Per-Asset Toggle</h2>
      <div className='grid md:grid-cols-4 gap-2'>
        {Object.keys(form.asset_enabled).map((symbol)=><label key={symbol} className='text-sm flex items-center gap-2'><input type='checkbox' checked={form.asset_enabled[symbol]} onChange={e=>setForm({...form, asset_enabled: {...form.asset_enabled, [symbol]: e.target.checked}})} />{symbol}</label>)}
      </div>
    </div>

    <button onClick={save} className='px-4 py-2 bg-cyan-700 rounded hover:bg-cyan-600'>Save Settings</button>
    {status && <span className='text-emerald-300 ml-3'>{status}</span>}
  </div>
}
