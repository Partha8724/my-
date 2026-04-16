import { NextResponse } from "next/server";
import { plannerSchema } from "@/lib/validators";

export async function POST(req: Request) {
  const body = plannerSchema.parse(await req.json());
  const plan = [
    `Daily ${body.hoursPerDay}h split: 45% concepts, 35% MCQ/test, 20% revision`,
    `Weekly: 1 full-length mock + 2 sectional tests for ${body.exam}`,
    `State focus: 2 sessions/week on ${body.state}-specific current affairs`
  ];
  return NextResponse.json({ plan });
}
