create extension if not exists "uuid-ossp";

create table users (
  id uuid primary key default uuid_generate_v4(),
  email text unique not null,
  role text not null default 'student' check (role in ('student','mentor','admin')),
  created_at timestamptz default now()
);

create table profiles (
  user_id uuid primary key references users(id) on delete cascade,
  full_name text not null,
  phone text,
  avatar_url text,
  preferred_language text not null default 'English',
  state_code text,
  target_exam_id uuid,
  daily_goal_hours int default 4,
  updated_at timestamptz default now()
);

create table states (
  id uuid primary key default uuid_generate_v4(),
  name text unique not null,
  code text unique not null,
  type text not null check (type in ('state','ut'))
);

create table languages (
  id uuid primary key default uuid_generate_v4(),
  code text unique not null,
  name text unique not null,
  is_active boolean default true
);

create table exams (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  slug text unique not null,
  category text not null,
  level text not null,
  overview text,
  eligibility text,
  notification_cycle text,
  created_at timestamptz default now()
);

create table subjects (
  id uuid primary key default uuid_generate_v4(),
  exam_id uuid references exams(id) on delete cascade,
  name text not null,
  weightage numeric(5,2)
);

create table topics (
  id uuid primary key default uuid_generate_v4(),
  subject_id uuid references subjects(id) on delete cascade,
  title text not null,
  difficulty int default 2,
  state_specific boolean default false
);

create table questions (
  id uuid primary key default uuid_generate_v4(),
  exam_id uuid references exams(id) on delete cascade,
  subject_id uuid references subjects(id),
  topic_id uuid references topics(id),
  language_code text,
  question_type text check (question_type in ('mcq','descriptive')),
  statement text not null,
  explanation text,
  difficulty int default 2,
  marks numeric(5,2) default 1,
  negative_marks numeric(5,2) default 0.33,
  year int,
  source text
);

create table options (
  id uuid primary key default uuid_generate_v4(),
  question_id uuid references questions(id) on delete cascade,
  option_key text not null,
  option_text text not null,
  is_correct boolean default false
);

create table test_attempts (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  exam_id uuid references exams(id),
  mode text check (mode in ('topic','section','full')),
  score numeric(6,2),
  accuracy numeric(5,2),
  started_at timestamptz,
  completed_at timestamptz,
  duration_seconds int
);

create table test_answers (
  id uuid primary key default uuid_generate_v4(),
  attempt_id uuid references test_attempts(id) on delete cascade,
  question_id uuid references questions(id),
  selected_option_id uuid references options(id),
  is_correct boolean,
  time_spent_seconds int
);

create table notes (
  id uuid primary key default uuid_generate_v4(),
  exam_id uuid references exams(id),
  state_id uuid references states(id),
  language_code text,
  title text not null,
  content_markdown text,
  tags text[],
  is_premium boolean default false,
  published_at timestamptz
);

create table pdf_resources (
  id uuid primary key default uuid_generate_v4(),
  exam_id uuid references exams(id),
  state_id uuid references states(id),
  language_code text,
  title text not null,
  file_url text not null,
  size_kb int,
  is_premium boolean default false
);

create table current_affairs (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  summary text not null,
  body text,
  scope text check (scope in ('national','state')),
  state_id uuid references states(id),
  published_on date not null,
  language_code text,
  tags text[]
);

create table subscriptions (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  plan text not null,
  status text not null,
  start_date date,
  end_date date,
  razorpay_customer_id text,
  razorpay_subscription_id text
);

create table payments (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  subscription_id uuid references subscriptions(id),
  amount_paise int not null,
  currency text default 'INR',
  provider text default 'razorpay',
  provider_order_id text,
  provider_payment_id text,
  payment_status text,
  paid_at timestamptz
);

create table bookmarks (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  entity_type text,
  entity_id uuid,
  created_at timestamptz default now()
);

create table study_plans (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  exam_id uuid references exams(id),
  state_id uuid references states(id),
  plan_json jsonb not null,
  generated_by text default 'ai',
  created_at timestamptz default now()
);

create table ai_chats (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  mode text,
  language_code text,
  exam_id uuid references exams(id),
  input_text text not null,
  output_text text,
  created_at timestamptz default now()
);

create table analytics (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id),
  event_name text not null,
  event_payload jsonb,
  created_at timestamptz default now()
);

create table weak_topics (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  topic_id uuid references topics(id),
  weakness_score numeric(5,2),
  last_seen timestamptz default now()
);

create table essay_submissions (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  exam_id uuid references exams(id),
  prompt text,
  answer_text text,
  ai_feedback jsonb,
  score numeric(5,2),
  submitted_at timestamptz default now()
);

create table admin_logs (
  id uuid primary key default uuid_generate_v4(),
  admin_user_id uuid references users(id),
  action text not null,
  entity_type text,
  entity_id uuid,
  metadata jsonb,
  created_at timestamptz default now()
);

alter table profiles add constraint fk_target_exam foreign key (target_exam_id) references exams(id);
