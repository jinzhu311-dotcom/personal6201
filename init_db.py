from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from db import init_db, counts
init_db()
print('Database initialised:', counts())
