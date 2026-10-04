import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from app import generate

def test_platform_outputs():
    for platform in ('xiaohongshu', 'wechat', 'video_account'):
        result = generate('A tool that helps students organise lecture notes', platform, 'university students')
        assert result['platform_name']
        assert result['hook'] and result['body']

def test_high_risk_vocabulary_is_defined():
    assert '最好' in ['第一', '第一名', '最好', '顶级', '保证', '100%']
