import Link from "next/link";

const links = [
  ["Exams", "/exams"],
  ["Dashboard", "/dashboard"],
  ["AI Assistant", "/ai-assistant"],
  ["Pricing", "/pricing"]
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-brand-950/90 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold text-cyan-300">OrbitGov AI</Link>
        <div className="flex items-center gap-6 text-sm text-slate-200">
          {links.map(([label, href]) => (
            <Link key={href} href={href} className="hover:text-cyan-300">{label}</Link>
          ))}
          <Link href="/signup" className="rounded-full bg-cyan-400 px-4 py-2 font-semibold text-slate-900">Start Free</Link>
        </div>
      </nav>
    </header>
  );
}
