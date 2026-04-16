import { HeroSection } from "@/components/sections/hero";
import { exams, languages, statesAndUTs } from "@/lib/data/catalog";

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <section className="mx-auto grid max-w-7xl gap-5 px-6 py-10 lg:grid-cols-3">
        <article className="glass rounded-2xl p-5"><h3 className="font-semibold">Exam Coverage</h3><p className="mt-2 text-slate-300">{exams.length}+ categories: UPSC to state PSC, police, teaching, and judiciary.</p></article>
        <article className="glass rounded-2xl p-5"><h3 className="font-semibold">Language Coverage</h3><p className="mt-2 text-slate-300">{languages.length} Indian languages with bilingual support mode.</p></article>
        <article className="glass rounded-2xl p-5"><h3 className="font-semibold">All India Reach</h3><p className="mt-2 text-slate-300">Coverage for {statesAndUTs.length} states and union territories.</p></article>
      </section>
    </>
  );
}
