from __future__ import annotations
import csv, json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / 'db' / 'pitchcraft.sqlite3'
SCHEMA = ROOT / 'db' / 'schema.sql'


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA.read_text(encoding='utf-8'))
        conn.executemany('INSERT OR IGNORE INTO banned_terms(term, reason) VALUES (?, ?)', [
            ('第一', '不可验证的绝对排名'), ('第一名', '不可验证的绝对排名'), ('最好', '不可验证的绝对比较'),
            ('顶级', '不可验证的绝对比较'), ('保证', '不当保证性承诺'), ('100%', '不当保证性承诺')
        ])


def import_csv(path: str | Path, is_eval_case=False):
    init_db()
    rows = list(csv.DictReader(Path(path).open(encoding='utf-8-sig', newline='')))
    required = {'brief_key','region','domain','brief_text','platform','hook','body','hashtags'}
    if rows and not required.issubset(rows[0]):
        raise ValueError(f'CSV is missing fields: {sorted(required - set(rows[0]))}')
    with connect() as conn:
        for r in rows:
            if r['region'] != 'CN':
                raise ValueError('The revised project accepts region=CN only')
            conn.execute('''INSERT INTO briefs(brief_key,region,domain,brief_text,target_user,key_advantage,is_eval_case,source_note)
                            VALUES(?,?,?,?,?,?,?,?)
                            ON CONFLICT(brief_key) DO UPDATE SET brief_text=excluded.brief_text,
                            target_user=excluded.target_user,key_advantage=excluded.key_advantage,
                            is_eval_case=excluded.is_eval_case,source_note=excluded.source_note''',
                         (r['brief_key'],r['region'],r['domain'],r.get('brief_text',''),r.get('target_user',''),r.get('key_advantage',''),int(r.get('is_eval_case') or is_eval_case),r.get('source_note','')))
            bid = conn.execute('SELECT id FROM briefs WHERE brief_key=?',(r['brief_key'],)).fetchone()['id']
            conn.execute('''INSERT INTO references_copy(brief_id,platform,hook,body,hashtags,cta,author_type)
                            VALUES(?,?,?,?,?,?,?) ON CONFLICT(brief_id,platform) DO UPDATE SET hook=excluded.hook,
                            body=excluded.body,hashtags=excluded.hashtags,cta=excluded.cta''',
                         (bid,r['platform'],r['hook'],r['body'],r.get('hashtags','[]'),r.get('cta',''),r.get('author_type','student_author')))
    return len(rows)


def counts():
    with connect() as conn:
        return dict(conn.execute('''SELECT (SELECT COUNT(*) FROM briefs) briefs,
          (SELECT COUNT(*) FROM references_copy) references_count,
          (SELECT COUNT(*) FROM briefs WHERE is_eval_case=1) eval_briefs''').fetchone())

if __name__ == '__main__':
    init_db()
    print(counts())
