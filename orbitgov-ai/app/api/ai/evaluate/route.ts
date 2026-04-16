import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = (await req.json()) as { answer?: string };
  const score = Math.min(10, Math.max(1, Math.floor((body.answer?.length ?? 0) / 120)));
  return NextResponse.json({ score, feedback: "Strengthen intro-context-link and conclude with actionable governance insight." });
}
