import Link from "next/link";

const links = [
  ["Home", "/"],
  ["Services", "/services"],
  ["Dashboard", "/dashboard"],
  ["Pricing", "/pricing"],
  ["Contact", "/contact"]
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-brand-950/90 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold text-cyan-300">
          OrbitGov AI
        </Link>
        <div className="flex flex-wrap items-center justify-end gap-x-5 gap-y-2 text-sm text-slate-200">
          {links.map(([label, href]) => (
            <Link key={href} href={href} className="hover:text-cyan-300">
              {label}
            </Link>
          ))}
          <Link href="/requirements" className="rounded-full bg-cyan-400 px-4 py-2 font-semibold text-slate-900">
            Upload Brief
          </Link>
        </div>
      </nav>
    </header>
  );
}
