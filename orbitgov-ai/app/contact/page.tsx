export default function ContactPage() {
  return (
    <section className="mx-auto flex w-full max-w-7xl flex-col gap-10 px-6 py-16 sm:gap-12 sm:py-20 lg:py-24">
      <header className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Contact</p>
        <h1 className="text-4xl font-semibold sm:text-5xl">Let’s scope your next AI delivery sprint.</h1>
        <p className="max-w-2xl text-slate-300">Share your goals and constraints, and our team will respond within one business day.</p>
      </header>

      <div className="grid gap-6 lg:grid-cols-2">
        <article className="glass rounded-2xl p-6">
          <h2 className="text-2xl font-semibold">Reach us</h2>
          <ul className="mt-4 space-y-3 text-slate-300">
            <li>Email: hello@orbitgov.ai</li>
            <li>Sales: +1 (415) 555-0174</li>
            <li>Hours: Monday–Friday, 9:00 AM to 6:00 PM PT</li>
          </ul>
        </article>
        <article className="glass rounded-2xl p-6">
          <h2 className="text-2xl font-semibold">Preferred contact flow</h2>
          <ol className="mt-4 space-y-3 text-slate-300">
            <li>1. Share your requirements through the upload page.</li>
            <li>2. We schedule a 30-minute discovery call.</li>
            <li>3. Receive a scoped delivery proposal with timeline.</li>
          </ol>
        </article>
      </div>
    </section>
  );
}
