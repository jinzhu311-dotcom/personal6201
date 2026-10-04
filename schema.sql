PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS briefs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brief_key TEXT NOT NULL UNIQUE,
  region TEXT NOT NULL DEFAULT 'CN' CHECK (region = 'CN'),
  domain TEXT NOT NULL,
  brief_text TEXT NOT NULL,
  target_user TEXT,
  key_advantage TEXT,
  source_note TEXT,
  is_eval_case INTEGER NOT NULL DEFAULT 0 CHECK (is_eval_case IN (0,1)),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS references_copy (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brief_id INTEGER NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
  platform TEXT NOT NULL CHECK (platform IN ('xiaohongshu','wechat','video_account')),
  hook TEXT NOT NULL,
  body TEXT NOT NULL,
  hashtags TEXT NOT NULL DEFAULT '[]',
  cta TEXT,
  author_type TEXT NOT NULL DEFAULT 'student_author',
  locked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (brief_id, platform)
);

CREATE TABLE IF NOT EXISTS generation_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brief_id INTEGER NOT NULL REFERENCES briefs(id),
  platform TEXT NOT NULL CHECK (platform IN ('xiaohongshu','wechat','video_account')),
  model_name TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  output_json TEXT NOT NULL,
  validation_json TEXT NOT NULL,
  abstained INTEGER NOT NULL DEFAULT 0 CHECK (abstained IN (0,1)),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  generation_run_id INTEGER NOT NULL REFERENCES generation_runs(id) ON DELETE CASCADE,
  rater_id TEXT NOT NULL CHECK (rater_id IN ('rater_a','rater_b')),
  tone_score INTEGER NOT NULL CHECK (tone_score BETWEEN 1 AND 5),
  completeness_score INTEGER NOT NULL CHECK (completeness_score BETWEEN 1 AND 5),
  factuality_score INTEGER NOT NULL CHECK (factuality_score BETWEEN 1 AND 5),
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (generation_run_id, rater_id)
);

CREATE TABLE IF NOT EXISTS banned_terms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  term TEXT NOT NULL UNIQUE,
  reason TEXT NOT NULL DEFAULT 'absolute_or_unverifiable_claim'
);

CREATE INDEX IF NOT EXISTS idx_references_platform ON references_copy(platform);
CREATE INDEX IF NOT EXISTS idx_briefs_eval ON briefs(is_eval_case);
CREATE INDEX IF NOT EXISTS idx_ratings_run ON ratings(generation_run_id);
