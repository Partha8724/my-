import { DashboardOverview } from "@/components/dashboard/overview";

export default function DashboardPage() {
  return (
    <section className="mx-auto max-w-7xl px-6 py-14">
      <h1 className="mb-6 text-3xl font-semibold">Student Dashboard</h1>
      <DashboardOverview />
    </section>
  );
}
