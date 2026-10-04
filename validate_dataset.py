from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from db import connect

with connect() as conn:
    briefs = conn.execute("SELECT COUNT(*) n FROM briefs WHERE is_eval_case=1").fetchone()['n']
    refs = conn.execute("SELECT COUNT(*) n FROM references_copy WHERE brief_id IN (SELECT id FROM briefs WHERE is_eval_case=1)").fetchone()['n']
    platforms = conn.execute("SELECT COUNT(DISTINCT platform) n FROM references_copy WHERE brief_id IN (SELECT id FROM briefs WHERE is_eval_case=1)").fetchone()['n']
print({'eval_briefs': briefs, 'eval_references': refs, 'platforms': platforms})
if (briefs, refs, platforms) != (40, 120, 3):
    raise SystemExit('Formal dataset requirement not met: 40 briefs, 120 reference copies and 3 platforms are required. Current data is demo-only.')
print('Formal dataset validation passed')
