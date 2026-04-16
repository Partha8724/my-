import { chatSchema } from "@/lib/validators";

const FALLBACK_REPLY =
  "I can help with study plans, revision strategy, and exam-specific practice. Share your exam and target date to get a detailed plan.";

type ChatResult = {
  reply: string;
  source: "mock" | "openai";
};

export async function generateAIResponse(payload: unknown): Promise<ChatResult> {
  const input = chatSchema.parse(payload);

  if (!process.env.OPENAI_API_KEY) {
    return {
      reply: `${FALLBACK_REPLY}\n\nYou said: ${input.message}`,
      source: "mock"
    };
  }

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL ?? "gpt-4o-mini",
      temperature: 0.3,
      messages: [
        {
          role: "system",
          content:
            "You are OrbitGov AI, an assistant for Indian competitive exam preparation. Provide concise, practical guidance."
        },
        {
          role: "user",
          content: input.message
        }
      ]
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`OpenAI request failed (${response.status}): ${errorText}`);
  }

  const data = (await response.json()) as {
    choices?: Array<{ message?: { content?: string } }>;
  };

  return {
    reply: data.choices?.[0]?.message?.content?.trim() || FALLBACK_REPLY,
    source: "openai"
  };
}
