const serviceCards = [
  {
    title: "AI Product Discovery",
    points: ["Stakeholder alignment workshops", "Problem framing and KPI mapping", "Delivery roadmap with phased milestones"]
  },
  {
    title: "Workflow Automation",
    points: ["CRM and support automation", "Internal ops assistants", "Human-in-the-loop review flows"]
  },
  {
    title: "Launch & Optimization",
    points: ["Go-live checklists", "Performance monitoring dashboards", "Quarterly iteration planning"]
  }
];

export default function ServicesPage() {
  return (
    <section className="mx-auto flex w-full max-w-7xl flex-col gap-10 px-6 py-16 sm:gap-12 sm:py-20 lg:py-24">
      <header className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Services</p>
        <h1 className="text-4xl font-semibold sm:text-5xl">End-to-end support for startup execution.</h1>
        <p className="max-w-3xl text-slate-300">
          Choose the engagement model that fits your stage, from early discovery to hands-on implementation and post-launch tuning.
        </p>
      </header>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {serviceCards.map((service) => (
          <article key={service.title} className="glass rounded-2xl p-6">
            <h2 className="text-2xl font-semibold">{service.title}</h2>
            <ul className="mt-4 space-y-2 text-slate-300">
              {service.points.map((point) => (
                <li key={point}>• {point}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
