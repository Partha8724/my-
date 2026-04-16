"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis } from "recharts";

const data = [
  { day: "Mon", score: 62 },
  { day: "Tue", score: 68 },
  { day: "Wed", score: 71 },
  { day: "Thu", score: 70 },
  { day: "Fri", score: 76 },
  { day: "Sat", score: 81 }
];

export function DashboardOverview() {
  return (
    <section className="grid gap-6 lg:grid-cols-3">
      <article className="glass rounded-2xl p-5"><p className="text-sm text-slate-400">Daily Target</p><p className="text-2xl font-semibold">6 Hours</p></article>
      <article className="glass rounded-2xl p-5"><p className="text-sm text-slate-400">Accuracy</p><p className="text-2xl font-semibold">81%</p></article>
      <article className="glass rounded-2xl p-5"><p className="text-sm text-slate-400">Streak</p><p className="text-2xl font-semibold">19 days</p></article>
      <article className="glass col-span-full rounded-2xl p-5">
        <h3 className="mb-4 text-lg font-semibold">Performance Trend</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}><CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" /><XAxis dataKey="day" /><Tooltip /><Area type="monotone" dataKey="score" stroke="#6AF0F8" fill="#6AF0F855" /></AreaChart>
          </ResponsiveContainer>
        </div>
      </article>
    </section>
  );
}
