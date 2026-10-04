from __future__ import annotations
import os
from flask import Flask, request, render_template_string
from db import connect, init_db

app = Flask(__name__)
init_db()
PLATFORMS = {
    'xiaohongshu': ('Xiaohongshu', 'Conversational first-person voice, light emoji use, 3–8 hashtags'),
    'wechat': ('WeChat Official Account', 'Structured argument, clear value proposition, measured tone'),
    'video_account': ('WeChat Video Account', 'Short spoken script, natural pauses, clear call to action'),
}

HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PitchCraft — AI Copywriting Workspace</title>
<style>
:root{--blue:#1677ff;--deep:#102a43;--ink:#1f2937;--muted:#6b778c;--line:#e8edf3;--bg:#f5f7fa;--orange:#ff7a45;--green:#12a66a;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:14px}
a{text-decoration:none;color:inherit}.topline{height:3px;background:linear-gradient(90deg,var(--blue),#52c41a,var(--orange))}
.nav{height:64px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center}.nav-inner{max-width:1180px;width:100%;margin:auto;padding:0 24px;display:flex;align-items:center;gap:34px}.logo{font-size:23px;font-weight:850;color:var(--deep);letter-spacing:-.8px}.logo span{color:var(--blue)}.nav-link{color:#5b6575;font-weight:600}.nav-link.active{color:var(--blue)}.nav-spacer{flex:1}.nav-pill{border:1px solid #d9e2ec;border-radius:20px;padding:8px 14px;color:#536173;font-weight:600;background:#fff}
.hero{position:relative;overflow:hidden;background:linear-gradient(120deg,#0e3970 0%,#1458a7 55%,#2585d8 100%);color:#fff}.hero:before,.hero:after{content:"";position:absolute;border-radius:50%;border:1px solid #ffffff25;pointer-events:none}.hero:before{width:360px;height:360px;right:-80px;top:-190px;box-shadow:0 0 0 28px #ffffff08,0 0 0 58px #ffffff05}.hero:after{width:210px;height:210px;left:42%;bottom:-170px;box-shadow:0 0 0 20px #ffffff08}.hero-inner{position:relative;z-index:1;max-width:1180px;margin:auto;padding:34px 24px 38px;display:flex;align-items:center;justify-content:space-between;gap:28px}.hero h1{font-size:30px;line-height:1.18;margin:0 0 11px;letter-spacing:-.6px}.hero p{margin:0;color:#dbeafe;max-width:670px;font-size:15px}.hero-badge{position:relative;background:#ffffff1c;border:1px solid #ffffff3d;border-radius:12px;padding:15px 18px;min-width:208px;box-shadow:0 14px 30px #061b3b33}.hero-badge strong{display:block;font-size:25px}.hero-badge small{color:#dbeafe}.hero-badge:after{content:"✦";position:absolute;right:14px;top:-12px;color:#ffd666;font-size:22px}
.container{max-width:1180px;margin:0 auto;padding:24px}.crumb{font-size:13px;color:#8492a6;margin-bottom:18px}.crumb b{color:#4d5c6f}.layout{display:grid;grid-template-columns:235px minmax(0,1fr);gap:20px;align-items:start}.side-card,.card{background:#fff;border:1px solid var(--line);border-radius:9px;box-shadow:0 2px 8px #102a4308}.side-card{overflow:hidden}.side-title{font-weight:800;padding:16px 18px;border-bottom:1px solid var(--line);color:var(--deep)}.side-item{padding:13px 18px;color:#64748b;display:flex;justify-content:space-between}.side-item.active{background:#eef6ff;color:var(--blue);border-left:3px solid var(--blue);padding-left:15px;font-weight:700}.side-note{margin-top:16px;padding:15px 16px;background:#fff8ed;border:1px solid #ffe1b8;border-radius:9px;color:#825b24;line-height:1.55;font-size:12px}.content{min-width:0}.section-heading{display:flex;justify-content:space-between;align-items:end;margin:0 0 12px}.section-heading h2{font-size:19px;margin:0;color:var(--deep)}.section-heading span{font-size:12px;color:var(--muted)}.generator{padding:22px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field label{display:flex;justify-content:space-between;font-size:12px;font-weight:800;color:#536173;margin-bottom:7px;text-transform:uppercase;letter-spacing:.45px}.field label em{font-style:normal;text-transform:none;letter-spacing:0;font-weight:500;color:#9aa6b5}.field textarea,.field input,.field select{width:100%;border:1px solid #ccd6e0;border-radius:6px;padding:11px 12px;background:#fff;color:var(--ink);font:inherit;outline:none;transition:.18s}.field textarea{resize:vertical;min-height:122px;line-height:1.55}.field textarea:focus,.field input:focus,.field select:focus{border-color:var(--blue);box-shadow:0 0 0 3px #1677ff18}.span-2{grid-column:1/-1}.actions{display:flex;align-items:center;gap:12px;margin-top:18px}.btn{border:0;border-radius:6px;padding:11px 22px;color:#fff;background:var(--blue);font-weight:800;font-size:14px;cursor:pointer;box-shadow:0 4px 10px #1677ff28}.btn:hover{background:#095fda}.hint{color:#8a96a6;font-size:12px}.mini-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}.mini{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px 16px}.mini strong{display:block;font-size:20px;color:var(--deep)}.mini span{font-size:12px;color:var(--muted)}
.result-card{margin-top:20px;padding:0;overflow:hidden}.result-top{padding:17px 22px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:11px}.result-top h2{font-size:17px;margin:0;color:var(--deep)}.tag{font-size:11px;font-weight:800;color:#1d5fbf;background:#edf5ff;border-radius:4px;padding:5px 8px}.result-body{padding:22px}.result-hook{font-size:20px;font-weight:800;color:var(--deep);margin:0 0 15px}.result-copy{border-left:3px solid #8bbcff;padding-left:15px;white-space:pre-wrap;line-height:1.75;color:#3c4858}.status{margin-top:18px;padding:11px 13px;border-radius:6px;font-size:12px;line-height:1.5}.ok{background:#effaf5;border:1px solid #bde8d3;color:#16734d}.warn{background:#fff7e8;border:1px solid #ffd591;color:#8c5b15}.disclaimer{color:#9aa6b5;font-size:11px;margin-top:14px}
.feature-strip{display:flex;gap:9px;flex-wrap:wrap;margin:-4px 0 19px}.feature-chip{background:#fff;border:1px solid var(--line);border-radius:18px;padding:7px 12px;color:#637083;font-size:12px;box-shadow:0 2px 8px #102a4305}.feature-chip b{color:var(--blue);margin-right:4px}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 18px}.step{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:9px;padding:11px 13px}.step-no{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:#eaf3ff;color:var(--blue);font-weight:850;font-size:12px}.step b{font-size:12px;color:var(--deep)}.step small{display:block;color:#8a96a6;font-size:11px;margin-top:2px}.info-row{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:20px}.info{padding:18px}.info h3{margin:0 0 8px;color:var(--deep);font-size:14px}.info p{margin:0;color:var(--muted);font-size:12px;line-height:1.65}.footer{max-width:1180px;margin:0 auto;padding:10px 24px 35px;color:#98a3b2;font-size:11px}
@media(max-width:760px){.nav-inner{gap:16px}.nav-link{display:none}.hero-inner{display:block}.hero-badge{margin-top:20px}.layout{grid-template-columns:1fr}.side-card{display:none}.form-grid,.info-row,.steps{grid-template-columns:1fr}.span-2{grid-column:auto}.mini-stats{grid-template-columns:1fr 1fr}.mini:last-child{grid-column:1/-1}}
</style>
</head>
<body><div class="topline"></div>
<header class="nav"><div class="nav-inner"><div class="logo">Pitch<span>Craft</span></div><a class="nav-link active" href="/">Workspace</a><a class="nav-link" href="#how">How it works</a><a class="nav-link" href="#about">About</a><div class="nav-spacer"></div><div class="nav-pill">English mode ▾</div></div></header>
<section class="hero"><div class="hero-inner"><div><h1>Make every project pitch<br>sound ready to publish.</h1><p>Turn one student project brief into platform-native promotional copy for three Chinese social platforms — in seconds.</p></div><div class="hero-badge"><strong>3 platforms</strong><small>One brief · multiple voices</small></div></div></section>
<main class="container"><div class="crumb">Home&nbsp;&nbsp;/&nbsp;&nbsp;<b>Copywriting workspace</b></div><div class="feature-strip"><div class="feature-chip"><b>✦</b>Platform-native tone</div><div class="feature-chip"><b>✓</b>Structured output</div><div class="feature-chip"><b>◉</b>Human review</div><div class="feature-chip"><b>↗</b>Ready to copy</div></div><div class="steps"><div class="step"><div class="step-no">1</div><div><b>Paste your brief</b><small>Describe the project</small></div></div><div class="step"><div class="step-no">2</div><div><b>Choose a voice</b><small>Select a platform</small></div></div><div class="step"><div class="step-no">3</div><div><b>Review the draft</b><small>Edit before publishing</small></div></div></div><div class="layout"><aside><div class="side-card"><div class="side-title">Workspace</div><div class="side-item active">Generate copy <span>›</span></div><div class="side-item">Reference library <span>›</span></div><div class="side-item">Evaluation plan <span>›</span></div><div class="side-item">Project settings <span>›</span></div></div><div class="side-note"><b>Designed for student teams</b><br>Keep the final decision and publishing step with a human reviewer.</div></aside>
<section class="content"><div class="section-heading"><h2>Generate platform-native copy</h2><span>Fast draft · human review required</span></div><div class="card generator"><form method="post"><div class="form-grid"><div class="field span-2"><label>Project brief <em>Required</em></label><textarea name="brief" placeholder="Example: A tool that turns university lecture notes into revision cards" required>{{brief}}</textarea></div><div class="field"><label>Target platform <em>Required</em></label><select name="platform">{% for k,(n,d) in platforms.items() %}<option value="{{k}}" {% if platform==k %}selected{% endif %}>{{n}}</option>{% endfor %}</select></div><div class="field"><label>Target user <em>Optional</em></label><input name="target_user" value="{{target_user}}" placeholder="e.g. university students"></div></div><div class="actions"><button class="btn" type="submit">Generate copy&nbsp; →</button><span class="hint">No auto-posting · no persistent user input</span></div></form></div>
<div class="mini-stats"><div class="mini"><strong>{{stats.briefs}}</strong><span>project briefs loaded</span></div><div class="mini"><strong>{{stats.references_count}}</strong><span>reference copy records</span></div><div class="mini"><strong>3</strong><span>supported platforms</span></div></div>
{% if result %}<div class="card result-card"><div class="result-top"><span class="tag">GENERATED DRAFT</span><h2>{{result.platform_name}}</h2></div><div class="result-body"><h3 class="result-hook">{{result.hook}}</h3><div class="result-copy">{{result.body}}{% if result.hashtags %}\n\n{{result.hashtags|join(' ')}}{% endif %}{% if result.cta %}\n\n{{result.cta}}{% endif %}</div>{% if result.warnings %}<div class="status warn"><b>Human review required</b><br>{{result.warnings|join('; ')}}</div>{% else %}<div class="status ok"><b>Structure checks passed</b> · Verify facts and wording before publication.</div>{% endif %}<div class="disclaimer">This is an English demonstration mode. The formal evaluation dataset remains Chinese platform-native reference copy.</div></div></div>{% endif %}
<div class="info-row" id="how"><div class="card info"><h3>How it works</h3><p>Paste a brief, choose a platform, then review a structured hook, body and call to action. The system keeps deterministic checks separate from creative generation.</p></div><div class="card info" id="about"><h3>Responsible by design</h3><p>PitchCraft does not auto-publish. High-risk promotional terms are flagged, and the final posting decision stays with the user.</p></div></div>
</section></div></main><div class="footer">PitchCraft MVP · An individual PE6201 project · English demonstration mode</div></body></html>'''


def banned_terms(text):
    with connect() as conn:
        terms = [r['term'] for r in conn.execute('SELECT term FROM banned_terms')]
    return [t for t in terms if t in text]


def generate(brief, platform, target_user=''):
    name, style = PLATFORMS[platform]
    user = target_user or 'the target users of the student startup'
    if platform == 'xiaohongshu':
        hook = 'Student builders, this can help you spend less time rewriting copy 📌'
        body = f'If you are {user}, it can be surprisingly hard to turn “what we built” into something people understand and want to explore.\n\n{brief}. Start with the real use case, explain the value in plain language, and make the story feel like a useful recommendation rather than a product manual.'
        hashtags = ['#studentstartup', '#productivitytools', '#projectstory']
        cta = 'Want to see the full idea? Leave a comment and let’s compare notes.'
    elif platform == 'wechat':
        hook = 'Make your project visible: start with one clear sentence'
        body = f'For {user}, a strong project introduction must do more than list features. It should help readers understand the problem, the solution and the value within a short reading session.\n\n{brief}. A useful structure is simple: introduce the situation, explain how the product responds, and close with a clear next step.'
        hashtags, cta = [], 'Explore the project concept and decide whether it fits your needs.'
    else:
        hook = 'In 30 seconds: what problem does your project actually solve?'
        body = f'If you are {user}, remember three lines. First, name the problem. Second, explain that {brief}. Third, tell people why it is worth trying now.\n\nReplace abstract features with a concrete moment from the user’s day. That is what makes a short video easier to understand and remember.'
        hashtags, cta = [], 'Save this framework for your next project pitch.'
    full = hook + body + cta
    warnings = [f'High-risk terms detected: {", ".join(banned_terms(full))}'] if banned_terms(full) else []
    return {'platform_name':name,'hook':hook,'body':body,'hashtags':hashtags,'cta':cta,'warnings':warnings}

@app.route('/', methods=['GET','POST'])
def index():
    result=None; brief=''; platform='xiaohongshu'; target_user=''
    if request.method == 'POST':
        brief=request.form.get('brief','').strip(); platform=request.form.get('platform','xiaohongshu'); target_user=request.form.get('target_user','').strip()
        if brief and platform in PLATFORMS: result=generate(brief,platform,target_user)
    with connect() as conn:
        stats=dict(conn.execute('''SELECT (SELECT COUNT(*) FROM briefs) briefs,(SELECT COUNT(*) FROM references_copy) references_count''').fetchone())
    return render_template_string(HTML, result=result, brief=brief, platform=platform, target_user=target_user, platforms=PLATFORMS, stats=stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','8501')), debug=False)
