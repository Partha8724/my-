import Link from "next/link";

const highlights = [
  {
    title: "Built for startup teams",
    copy: "Ship AI features faster with reusable workflows for onboarding, support, and knowledge automation."
  },
  {
    title: "Production-ready delivery",
    copy: "From requirement intake to implementation plans, keep work visible across product, ops, and founders."
  },
  {
    title: "Secure by design",
    copy: "Role-based access, audit-friendly workflows, and clear handoff checkpoints for growing organizations."
  }
];

export default function HomePage() {
  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-16 px-6 py-16 sm:gap-20 sm:py-20 lg:py-24">
      <section className="grid items-center gap-10 lg:grid-cols-2 lg:gap-12">
        <div className="space-y-6">
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">OrbitGov AI Studio</p>
          <h1 className="text-4xl font-semibold leading-tight sm:text-5xl">Build startup-grade AI workflows without the chaos.</h1>
          <p className="max-w-2xl text-base text-slate-300 sm:text-lg">
            OrbitGov AI helps founders and product teams move from ideas to launch with structured services, transparent pricing,
            and clear requirement capture.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link href="/services" className="rounded-full bg-cyan-400 px-5 py-2.5 font-semibold text-slate-900">
              Explore Services
            </Link>
            <Link href="/requirements" className="rounded-full border border-white/20 px-5 py-2.5 font-semibold text-slate-100">
              Upload Requirements
            </Link>
          </div>
        </div>
        <div className="glass rounded-3xl p-6 sm:p-8">
          <h2 className="text-xl font-semibold">What you get</h2>
          <ul className="mt-5 space-y-4 text-slate-300">
            <li>• Guided discovery sessions for roadmap and architecture alignment.</li>
            <li>• Sprint-based implementation support with measurable milestones.</li>
            <li>• Documentation, handoff, and feedback loops for sustainable growth.</li>
          </ul>
        </div>
      </section>

      <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {highlights.map((item) => (
          <article key={item.title} className="glass rounded-2xl p-6">
            <h3 className="text-xl font-semibold">{item.title}</h3>
            <p className="mt-3 text-slate-300">{item.copy}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
