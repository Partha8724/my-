const plans = [
  {
    name: "Starter",
    price: "$799/mo",
    features: ["Bi-weekly strategy sync", "Requirement intake + prioritization", "1 active delivery stream"]
  },
  {
    name: "Growth",
    price: "$1,999/mo",
    features: ["Weekly execution sprints", "Dedicated product + implementation support", "3 active delivery streams"]
  },
  {
    name: "Scale",
    price: "Custom",
    features: ["Multi-team operating model", "Security and compliance assistance", "Custom success metrics and reporting"]
  }
];

export default function PricingPage() {
  return (
    <section className="mx-auto flex w-full max-w-7xl flex-col gap-10 px-6 py-16 sm:gap-12 sm:py-20 lg:py-24">
      <header className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Pricing</p>
        <h1 className="text-4xl font-semibold sm:text-5xl">Simple pricing that scales with your startup.</h1>
      </header>

      <div className="grid gap-5 lg:grid-cols-3">
        {plans.map((plan) => (
          <article key={plan.name} className="glass rounded-2xl p-6">
            <h2 className="text-2xl font-semibold">{plan.name}</h2>
            <p className="mt-2 text-3xl font-semibold text-cyan-300">{plan.price}</p>
            <ul className="mt-4 space-y-2 text-slate-300">
              {plan.features.map((feature) => (
                <li key={feature}>• {feature}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
