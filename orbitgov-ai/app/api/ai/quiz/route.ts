import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json({
    quiz: [
      { q: "Directive Principles belong to which part of the Constitution?", a: "Part IV" },
      { q: "Repo rate is decided by which body?", a: "RBI Monetary Policy Committee" }
    ]
  });
}
