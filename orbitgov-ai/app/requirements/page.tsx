export default function RequirementsPage() {
  return (
    <section className="mx-auto flex w-full max-w-5xl flex-col gap-10 px-6 py-16 sm:gap-12 sm:py-20 lg:py-24">
      <header className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Client Requirement Upload</p>
        <h1 className="text-4xl font-semibold sm:text-5xl">Upload project requirements in one place.</h1>
        <p className="text-slate-300">Submit context, goals, and assets so we can prepare an accurate implementation plan.</p>
      </header>

      <form className="glass grid gap-5 rounded-2xl p-6 sm:grid-cols-2 sm:p-8" aria-label="Client requirements form">
        <label className="flex flex-col gap-2 text-sm sm:col-span-1">
          Company name
          <input className="rounded-xl border border-white/20 bg-brand-950 px-4 py-3 text-slate-100" type="text" placeholder="Acme Labs" />
        </label>
        <label className="flex flex-col gap-2 text-sm sm:col-span-1">
          Contact email
          <input className="rounded-xl border border-white/20 bg-brand-950 px-4 py-3 text-slate-100" type="email" placeholder="founder@acme.com" />
        </label>
        <label className="flex flex-col gap-2 text-sm sm:col-span-2">
          Project summary
          <textarea className="min-h-32 rounded-xl border border-white/20 bg-brand-950 px-4 py-3 text-slate-100" placeholder="Describe the problem, users, timeline, and constraints." />
        </label>
        <label className="flex flex-col gap-2 text-sm sm:col-span-2">
          Upload brief (PDF/DOCX)
          <input className="rounded-xl border border-dashed border-white/20 bg-brand-950 px-4 py-3 text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-900" type="file" />
        </label>
        <button type="submit" className="rounded-full bg-cyan-400 px-5 py-3 font-semibold text-slate-900 sm:col-span-2 sm:w-fit">
          Submit Requirements
        </button>
      </form>
    </section>
  );
}
