"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { HeroScene } from "@/components/3d/hero-scene";

export function HeroSection() {
  return (
    <section className="mx-auto grid max-w-7xl gap-10 px-6 py-16 lg:grid-cols-2">
      <div className="space-y-6">
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="inline-block rounded-full border border-cyan-300/30 px-4 py-2 text-xs text-cyan-300">
          Premium AI Platform for Indian Government Exams
        </motion.p>
        <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-4xl font-bold leading-tight lg:text-6xl">
          Prepare smarter for UPSC, SSC, Banking, Railways & Every State Exam.
        </motion.h1>
        <p className="text-slate-300">Multilingual AI mentor, adaptive mock tests, weak-topic analytics, current affairs, and answer-writing feedback in one premium workspace.</p>
        <div className="flex gap-4">
          <Link href="/signup" className="rounded-full bg-cyan-400 px-6 py-3 font-semibold text-slate-900">Get Started</Link>
          <Link href="/ai-assistant" className="rounded-full border border-white/20 px-6 py-3">Try AI Assistant</Link>
        </div>
      </div>
      <HeroScene />
    </section>
  );
}
