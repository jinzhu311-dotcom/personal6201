from pathlib import Path
import argparse, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from db import import_csv, counts

parser = argparse.ArgumentParser()
parser.add_argument('csv_path')
parser.add_argument('--eval', action='store_true', help='Mark imported briefs as evaluation briefs')
args = parser.parse_args()
print(f'Imported {import_csv(args.csv_path, args.eval)} reference rows')
print(counts())
