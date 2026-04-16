# OrbitGov AI

Production-ready foundation for a premium AI-first Indian government exam preparation platform.

## 1) Project Folder Structure

```txt
orbitgov-ai/
  app/
    api/ai/{chat,plan,quiz,evaluate}/route.ts
    about/ contact/ exams/ state-exams/ syllabus/
    previous-year-questions/ mock-tests/ test-result/
    dashboard/ ai-assistant/ current-affairs/
    notes-library/ pdf-library/ pricing/ login/ signup/
    profile/ subscription/
    admin/{users,exams,questions,notes,current-affairs,analytics}/
    layout.tsx page.tsx globals.css
  components/
    3d/hero-scene.tsx
    sections/hero.tsx
    dashboard/overview.tsx
    ai/assistant-panel.tsx
    layout/{navbar,footer}.tsx
  lib/
    ai/orchestrator.ts
    auth/roles.ts
    payments/razorpay.ts
    data/catalog.ts
    validators/index.ts
    utils.ts
  supabase/
    schema.sql
    seed.sql
  middleware.ts
  .env.example
```

## 2) Complete Architecture Plan

- **Frontend**: Next.js App Router + TypeScript + Tailwind + Framer Motion + React Three Fiber.
- **Backend**: Next Route Handlers for AI orchestration, planner generation, quiz, and evaluation.
- **Data layer**: Supabase Postgres schema with exam-domain normalized tables.
- **Auth**: Cookie/session-based protected route middleware + role model (`student`, `mentor`, `admin`).
- **Payments**: Razorpay order creation helper with mock fallback in local/dev.
- **Admin**: Dedicated `/admin/*` namespace for management operations.

## 3) Database Schema

See `supabase/schema.sql` for all required entities:
users, profiles, exams, states, languages, subjects, topics, questions, options, test_attempts, test_answers, notes, pdf_resources, current_affairs, subscriptions, payments, bookmarks, study_plans, ai_chats, analytics, weak_topics, essay_submissions, admin_logs.

## 4) Auth Flow

1. User signs up/login (Supabase Auth integration expected).
2. Session cookie `orbitgov_session` is set.
3. Middleware protects `/dashboard`, `/ai-assistant`, `/subscription`, `/admin`.
4. Unauthorized users are redirected to `/login?next=<path>`.
5. Role checks are handled via `lib/auth/roles.ts` in server actions/routes.

## 5) Payment Flow

1. Frontend requests plan purchase.
2. Backend calls `createRazorpayOrder` with amount and receipt.
3. Razorpay checkout completes payment.
4. Webhook updates `payments` and `subscriptions`.
5. Dashboard reflects active premium features.

## 6) Multilingual Setup

- Supported languages are modeled in `languages` table + `lib/data/catalog.ts`.
- All content entities include language code columns.
- AI route accepts language and responds in selected language.
- Architecture supports incremental rollout of additional Indian languages.

## 7) AI Module Architecture

- `app/api/ai/chat`: context-aware mentor responses.
- `app/api/ai/plan`: study planner generation.
- `app/api/ai/quiz`: quiz generation endpoint.
- `app/api/ai/evaluate`: answer-writing evaluation endpoint.
- `lib/ai/orchestrator.ts`: provider abstraction + fallback + prompt safety tone.

## 8) Premium Homepage Design Structure

- 3D hero with torus orb, glow lighting, orbit controls.
- Motion intro badge/headline CTA using Framer Motion.
- Coverage cards for exams/languages/state footprint.
- Trust statement reinforcing honest AI messaging.

## 9) Dashboard Design Structure

- KPI glass cards for target/accuracy/streak.
- Recharts-based trend visualization.
- Extendable zones for weak topics, bookmarks, current affairs, and recommendations.

## 10) 3D Animation Implementation Structure

- `components/3d/hero-scene.tsx` hosts R3F canvas.
- Distorted torus object for AI-orb identity.
- Auto-rotation + float motion.
- DPR capped for performance (`dpr={[1,1.5]}`).

## 11) Reusable UI Component System

- Shared layout primitives (`Navbar`, `Footer`).
- Domain components (`HeroSection`, `DashboardOverview`, `AssistantPanel`).
- Utility `cn` helper for composable class names.

## 12) Admin Panel Structure

- Routes under `/admin/*`:
  - users, exams, questions, notes, current-affairs, analytics.
- Extend with role-gated server actions and audit log writes to `admin_logs`.

## 13) Working Route System

All required routes are scaffolded and render functional pages with production-safe structure.

## 14) Seed / Sample Data

`supabase/seed.sql` includes starter languages, states, and exams.

## 15) Environment Variable Example

See `.env.example` for Supabase, OpenAI, Razorpay, DB, and app URL config.

## 16) Setup Guide

```bash
npm install
cp .env.example .env.local
npm run dev
```

## 17) Deployment Instructions

- Deploy on Vercel.
- Set all environment variables in project settings.
- Run Supabase migration with `schema.sql` then `seed.sql`.
- Configure Razorpay webhook to deployment `/api/webhooks/razorpay` (to be added in integration phase).

## 18) QA Checklist

- [ ] Route navigation works on desktop/mobile.
- [ ] Protected route redirects work.
- [ ] AI endpoints validate payloads and return structured JSON.
- [ ] SQL migrations execute without errors.
- [ ] Payment flow handles success/failure/webhook retries.
- [ ] Accessibility: heading hierarchy, color contrast, focus states.

## 19) Performance Checklist

- [ ] 3D scene lazy-load if added to additional pages.
- [ ] Keep mesh complexity low.
- [ ] Use dynamic imports for heavy charts/scenes.
- [ ] Avoid expensive rerenders (memoization).
- [ ] Validate Lighthouse performance on mid-tier Android.

## 20) Production Readiness Foundation

This repo provides a deployable, modular base covering:
- route architecture,
- DB domain model,
- AI extensibility,
- payment abstraction,
- multilingual content strategy,
- premium UI baseline with 3D hero.

