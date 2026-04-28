const metrics = [
  { label: "Active projects", value: "12" },
  { label: "Avg. cycle time", value: "9 days" },
  { label: "On-time delivery", value: "96%" },
  { label: "Client satisfaction", value: "4.8/5" }
];

export default function DashboardPage() {
  return (
    <section className="mx-auto flex w-full max-w-7xl flex-col gap-10 px-6 py-16 sm:gap-12 sm:py-20 lg:py-24">
      <header className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Dashboard</p>
        <h1 className="text-4xl font-semibold sm:text-5xl">Delivery visibility for founders and operators.</h1>
        <p className="max-w-3xl text-slate-300">
          Track project status, delivery health, and team throughput in one view designed for fast startup decisions.
        </p>
      </header>

      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => (
          <article key={metric.label} className="glass rounded-2xl p-6">
            <p className="text-sm text-slate-400">{metric.label}</p>
            <p className="mt-2 text-3xl font-semibold">{metric.value}</p>
          </article>
        ))}
      </div>

      <article className="glass rounded-2xl p-6 sm:p-8">
        <h2 className="text-2xl font-semibold">Upcoming milestones</h2>
        <ul className="mt-4 space-y-3 text-slate-300">
          <li>• API integration review — Thursday, 10:00 AM UTC</li>
          <li>• Requirement validation workshop — Friday, 2:00 PM UTC</li>
          <li>• Sprint retro and scope planning — Monday, 9:00 AM UTC</li>
        </ul>
      </article>
    </section>
  );
}
