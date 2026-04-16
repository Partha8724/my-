"use client";

import { useState } from "react";

export function AssistantPanel() {
  const [message, setMessage] = useState("Explain fiscal deficit for UPSC beginner in Hindi.");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    const res = await fetch("/api/ai/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, mode: "doubt", language: "Hindi", exam: "UPSC" })
    });
    const data = await res.json();
    setAnswer(data.text ?? "No response");
    setLoading(false);
  };

  return (
    <section className="glass rounded-2xl p-6">
      <h2 className="text-xl font-semibold">AI Assistant Workspace</h2>
      <textarea className="mt-4 h-28 w-full rounded-xl bg-slate-900 p-3" value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={submit} className="mt-4 rounded-full bg-cyan-400 px-5 py-2 font-semibold text-slate-900">{loading ? "Thinking..." : "Ask OrbitGov AI"}</button>
      {answer && <pre className="mt-4 whitespace-pre-wrap rounded-xl border border-white/10 p-4 text-sm text-slate-200">{answer}</pre>}
    </section>
  );
}
