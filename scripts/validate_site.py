#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import re, subprocess, tempfile, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
REQUIRED=['index.html','about.html','services.html','solutions.html','contact.html','blog.html','guide.html','privacy.html','terms.html','blog-clinic-agent.html','blog-n8n-vs-make.html','blog-agent-vs-employee.html']
GA='G-6P2CM4PPHQ'
LOGO='assets/insiyab-mark-v4.svg?v=5'
errors=[]

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.refs=[]; self.scripts=[]; self._script=False; self._script_type=''; self._script_src=False; self._buf=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('a','link') and d.get('href'): self.refs.append(d['href'])
        if tag in ('img','script','source') and d.get('src'): self.refs.append(d['src'])
        if tag=='script': self._script=True; self._script_type=d.get('type',''); self._script_src=bool(d.get('src')); self._buf=[]
    def handle_data(self,data):
        if self._script: self._buf.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self._script:
            if not self._script_src and self._script_type not in ('application/ld+json','application/json'):
                js=''.join(self._buf).strip()
                if js: self.scripts.append(js)
            self._script=False; self._buf=[]

def local_target(href,current):
    h=href.strip()
    if not h or h.startswith(('#','mailto:','tel:','javascript:','data:')): return None
    u=urlparse(h)
    if u.scheme or u.netloc: return None
    path=unquote(u.path)
    if not path: return None
    target=(current.parent/path).resolve()
    try: target.relative_to(ROOT.resolve())
    except ValueError: return None
    if path.endswith('/'): target=target/'index.html'
    return target

for name in REQUIRED:
    p=ROOT/name
    if not p.is_file(): errors.append(f'missing required page: {name}'); continue
    s=p.read_text(encoding='utf-8',errors='ignore')
    if 'data:image/png;base64' in s: errors.append(f'embedded base64 image remains: {name}')
    if '?v=5?v=5' in s: errors.append(f'bad cache-busting URL: {name}')
    if s.count('rel="canonical"')!=1: errors.append(f'canonical count != 1: {name}')
    if len(re.findall(r'<meta\s+name=["\']description["\']',s,re.I))!=1: errors.append(f'description count != 1: {name}')
    if GA not in s: errors.append(f'analytics missing: {name}')
    if LOGO not in s: errors.append(f'clean logo not referenced: {name}')
    schema_count=len(re.findall(r'application/ld\+json',s,re.I))
    expected=2 if name.startswith('blog-') else 1
    if schema_count!=expected: errors.append(f'schema count {schema_count}, expected {expected}: {name}')
    if name=='index.html' and len(re.findall(r'hreflang=',s,re.I))!=3: errors.append('homepage hreflang count != 3')
    parser=AuditParser()
    try: parser.feed(s)
    except Exception as e: errors.append(f'HTML parser error {name}: {e}'); continue
    for ref in parser.refs:
        t=local_target(ref,p)
        if t and not t.exists(): errors.append(f'broken local reference in {name}: {ref}')
    for i,js in enumerate(parser.scripts):
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(js); fn=f.name
        r=subprocess.run(['node','--check',fn],capture_output=True,text=True)
        Path(fn).unlink(missing_ok=True)
        if r.returncode: errors.append(f'JavaScript syntax error {name} script {i+1}: {r.stderr.splitlines()[-1] if r.stderr else "unknown"}')

for f in ('robots.txt','sitemap.xml','CNAME','assets/insiyab-mark-v4.svg'):
    if not (ROOT/f).is_file(): errors.append(f'missing deployment asset: {f}')

if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'Quality gate passed: {len(REQUIRED)} pages, links, metadata, logo and inline JavaScript validated.')
