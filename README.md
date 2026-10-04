# PitchCraft (Individual Project MVP)

PitchCraft turns a student project brief into **platform-native promotional copy** for Xiaohongshu, WeChat Official Accounts and WeChat Video Account. The revised scope is limited to **Chinese reference data, 120 reference copies, no Singapore arm and no A/B experiment**.

## 1. Run the application

```bash
cd /home/ubuntu/pitchcraft
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 scripts/init_db.py
python3 app/app.py
```

Open `http://127.0.0.1:8501`.

For a one-command local start on macOS or Linux:

```bash
chmod +x run_local.sh
./run_local.sh
```

## 2. Database

SQLite file: `db/pitchcraft.sqlite3`.

- `briefs`: project briefs; only `region=CN` is accepted.
- `references_copy`: one locked reference copy per brief and platform.
- `generation_runs`: model/rule output and validation results.
- `ratings`: blind ratings from two independent raters, `rater_a` and `rater_b`.
- `banned_terms`: absolute promotional and inappropriate guarantee terms.

Import the author-locked reference dataset:

```bash
python3 scripts/import_csv.py /path/to/chinese_references.csv --eval
```

The CSV fields are shown in `seed/reference_template.csv`. The formal dataset must contain **40 Chinese project briefs × 3 platforms = 120 reference copies**. The three rows in the template are demo rows only and do not count toward the formal evaluation.

Validate the formal dataset:

```bash
python3 scripts/validate_dataset.py
```

## 3. Evaluation discipline

1. Lock all 120 ground-truth reference copies before running any model.
2. Do not place evaluation briefs in the few-shot reference set; retain `brief_key` for programmatic leakage checks.
3. Use two independent blind raters; the author must not rate their own system.
4. Report platform-native tone on a 1–5 scale and information completeness.
5. Compare PitchCraft against a fixed-template baseline on exactly the same briefs. A baseline win is still a finding.

## 4. Current boundary

This is a runnable MVP. The offline rule generator can later be replaced by a course-approved rented LLM while keeping the same database, output checks and evaluation protocol. The system does not auto-publish, persist user input, or process payments.
