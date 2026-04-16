import { NextResponse } from "next/server";
import { generateAIResponse } from "@/lib/ai/orchestrator";

export async function POST(req: Request) {
  try {
    const payload = await req.json();
    const data = await generateAIResponse(payload);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Unable to generate response", details: `${error}` }, { status: 400 });
  }
}
