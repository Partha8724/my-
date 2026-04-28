import Link from "next/link";

const quickLinks = [
  ["Home", "/"],
  ["Services", "/services"],
  ["Pricing", "/pricing"],
  ["Requirements", "/requirements"],
  ["Contact", "/contact"]
];

export function Footer() {
  return (
    <footer className="mt-20 border-t border-white/10 py-10 sm:py-12">
      <div className="mx-auto grid max-w-7xl gap-8 px-6 text-sm text-slate-400 md:grid-cols-2">
        <div>
          <p className="text-base font-semibold text-slate-200">OrbitGov AI</p>
          <p className="mt-3 max-w-md">Startup-focused AI delivery partner for product discovery, implementation, and scaling.</p>
        </div>
        <div>
          <p className="text-base font-semibold text-slate-200">Quick links</p>
          <div className="mt-3 flex flex-wrap gap-4">
            {quickLinks.map(([label, href]) => (
              <Link key={href} href={href} className="hover:text-cyan-300">
                {label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
