#!/usr/bin/env python3
from pathlib import Path
import re, json, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://insiyabtech.com.sa'
LOGO = 'assets/insiyab-mark-v4.svg?v=5'
OGIMG = BASE + '/assets/insiyab-mark.png?v=5'
GA_ID = 'G-6P2CM4PPHQ'

META = {
'index.html':('انسياب تيك | ذكاء اصطناعي وأتمتة وتكامل أنظمة','نبني حلول ذكاء اصطناعي وأتمتة وتكامل أنظمة تعمل داخل عملياتك الفعلية، من الوكلاء الذكيين إلى التحليلات ودعم القرار.'),
'about.html':('من نحن | انسياب تيك','تعرّف على انسياب تيك ومنهجنا في بناء حلول ذكاء اصطناعي وأتمتة عملية تربط الأنظمة والبيانات والتنفيذ داخل المؤسسات.'),
'services.html':('الخدمات | انسياب تيك','خدمات الذكاء الاصطناعي والأتمتة وتكامل الأنظمة وتحليل البيانات، مصممة حسب احتياج الشركات والجهات في السعودية.'),
'solutions.html':('الحلول | انسياب تيك','حلول وكلاء ذكاء اصطناعي وأتمتة وتكامل أنظمة وتحليلات ودعم قرار تُبنى حول العمل الحقيقي وقابلة للتوسع.'),
'contact.html':('تواصل معنا | انسياب تيك','تواصل مع انسياب تيك لمناقشة احتياجك في الذكاء الاصطناعي والأتمتة وتكامل الأنظمة وبناء نموذج أولي عملي.'),
'blog.html':('المعرفة والمدونة | انسياب تيك','مقالات تطبيقية عن الذكاء الاصطناعي والأتمتة والوكلاء الذكيين وتكامل الأنظمة من واقع التطبيق في السوق السعودي.'),
'guide.html':('الدليل التطبيقي | انسياب تيك','دليل عربي تطبيقي لفهم وبناء واستخدام وكلاء الذكاء الاصطناعي والأتمتة داخل الأعمال السعودية.'),
'blog-clinic-agent.html':('وكيل خدمة العملاء الذكي للعيادات | انسياب تيك','تجربة عملية توضح كيف يمكن لوكيل ذكي أتمتة نسبة كبيرة من استفسارات العملاء والحجوزات والمتابعة.'),
'blog-n8n-vs-make.html':('n8n أم Make.com؟ مقارنة عملية | انسياب تيك','مقارنة عملية بين n8n وMake.com من حيث المرونة والتكلفة والتكامل واختيار الأداة المناسبة للأتمتة.'),
'blog-agent-vs-employee.html':('وكيل ذكي أم موظف؟ مقارنة عملية | انسياب تيك','مقارنة عملية بين تكلفة وقدرات وكيل الذكاء الاصطناعي والموظف في المهام المتكررة وخدمة العملاء.'),
'privacy.html':('سياسة الخصوصية | انسياب تيك','سياسة الخصوصية الخاصة بموقع وخدمات انسياب تيك وكيفية التعامل مع البيانات والمعلومات.'),
'terms.html':('الشروط والأحكام | انسياب تيك','الشروط والأحكام المنظمة لاستخدام موقع وخدمات انسياب تيك.'),
}
LEGACY = set(META) - {'index.html','solutions.html'}

POLISH = '''<style id="insiyab-global-polish">
:root{--gold:#ff8a00!important;--gold-bright:#ff9f1a!important;--gold-dark:#d95f00!important;--gold-soft:#fff1e7!important;--coral:#ff5a47!important;--violet:#f3006f!important;--violet-soft:#ffe2ef!important;--grad-warm:linear-gradient(105deg,#ff8a00 0%,#ff5a47 48%,#f3006f 100%)!important;--grad-primary:linear-gradient(105deg,#ff8a00 0%,#ff5a47 48%,#f3006f 100%)!important}
.it-nav-lang{font-family:Poppins,system-ui,sans-serif!important;font-size:.72rem!important;letter-spacing:.03em!important;border:1px solid rgba(15,23,41,.12);border-radius:10px;padding:8px 11px!important}.it-nav-lang:hover{border-color:#ff5a47!important}.brand img{filter:none!important;mix-blend-mode:normal!important;opacity:1!important}.nav-inner{gap:14px}.nav-links{gap:14px!important}.nav-links a{white-space:nowrap}a:focus-visible,button:focus-visible{outline:3px solid rgba(255,90,71,.35)!important;outline-offset:3px!important}
@media(max-width:1180px){.nav-links{gap:10px!important}.nav-links a{font-size:.82rem!important}.it-nav-lang{padding:7px 9px!important}}@media(max-width:980px){.it-nav-lang{border:0;padding:12px 0!important}}
</style>'''

GA = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>'''
ORG = {"@context":"https://schema.org","@type":"Organization","name":"InsiyabTech","alternateName":"انسياب تيك","url":BASE,"logo":OGIMG,"email":"info@insiyabtech.com.sa","sameAs":["https://x.com/insiyabtech","https://www.instagram.com/insiyabtech/","https://www.tiktok.com/@insiyabtech"]}

def escape_attr(v):
    return v.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')

def nav_for(fname):
    items=[('index.html','الرئيسية'),('about.html','من نحن'),('services.html','الخدمات'),('solutions.html','الحلول'),('index.html#work','نماذج الأعمال'),('blog.html','المعرفة'),('contact.html','تواصل معنا')]
    out=['<ul class="nav-links">']
    for href,label in items:
        active=(href.split('#')[0]==fname) or (fname.startswith('blog-') and href=='blog.html')
        attrs=' class="active" aria-current="page"' if active else ''
        out.append(f'<li><a href="{href}"{attrs}>{label}</a></li>')
    out.append('<li><a href="index.html" class="it-nav-lang" onclick="try{localStorage.setItem(\'insiyab-lang\',\'en\')}catch(e){}">ENGLISH</a></li>')
    out.append('</ul>')
    return ''.join(out)

def clean_logo(s):
    s = re.sub(r'data:image/png;base64,[A-Za-z0-9+/=]+', LOGO, s)
    s = re.sub(r'(?<=["\'])assets/insiyab-mark\.(?:webp|png)(?:\?[^"\']*)?', LOGO, s)
    s = re.sub(r'(?<=["\'])assets/insiyab-mark-v4\.svg(?:\?v=\d+)?', LOGO, s)
    s = s.replace('type="image/png" href="'+LOGO+'"','type="image/svg+xml" href="'+LOGO+'"')
    return s

def inject_meta(s, fname, title, desc):
    canonical = BASE+'/' if fname == 'index.html' else f'{BASE}/{fname}'
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1, flags=re.S|re.I)
    s = re.sub(r'<meta\s+name=["\']description["\'][^>]*>\s*', '', s, flags=re.I)
    s = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>\s*', '', s, flags=re.I)
    s = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*hreflang=[^>]*>\s*', '', s, flags=re.I)
    s = re.sub(r'<meta\s+(?:property=["\']og:[^"\']+["\']|name=["\']twitter:[^"\']+["\'])[^>]*>\s*', '', s, flags=re.I)
    s = re.sub(r'<script\s+type=["\']application/ld\+json["\'][^>]*>.*?https://schema\.org.*?</script>\s*', '', s, flags=re.S|re.I)
    s = re.sub(r'<meta\s+name=["\']referrer["\'][^>]*>\s*', '', s, flags=re.I)
    block = [f'<meta name="description" content="{escape_attr(desc)}">','<meta name="referrer" content="strict-origin-when-cross-origin">',f'<link rel="canonical" href="{canonical}">','<meta property="og:locale" content="ar_SA">',f'<meta property="og:type" content="{"article" if fname.startswith("blog-") else "website"}">','<meta property="og:site_name" content="InsiyabTech">',f'<meta property="og:title" content="{escape_attr(title)}">',f'<meta property="og:description" content="{escape_attr(desc)}">',f'<meta property="og:url" content="{canonical}">',f'<meta property="og:image" content="{OGIMG}">','<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{escape_attr(title)}">',f'<meta name="twitter:description" content="{escape_attr(desc)}">',f'<meta name="twitter:image" content="{OGIMG}">','<script type="application/ld+json">'+json.dumps(ORG,ensure_ascii=False,separators=(',',':'))+'</script>']
    if fname == 'index.html': block += [f'<link rel="alternate" hreflang="ar" href="{canonical}">',f'<link rel="alternate" hreflang="en" href="{canonical}">',f'<link rel="alternate" hreflang="x-default" href="{canonical}">']
    if fname.startswith('blog-'):
        h = re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S|re.I)
        headline = re.sub('<[^>]+>',' ',h.group(1)).strip() if h else title
        article={"@context":"https://schema.org","@type":"Article","headline":headline,"inLanguage":"ar-SA","mainEntityOfPage":canonical,"publisher":{"@type":"Organization","name":"InsiyabTech","logo":{"@type":"ImageObject","url":OGIMG}}}
        block.append('<script type="application/ld+json">'+json.dumps(article,ensure_ascii=False,separators=(',',':'))+'</script>')
    return s.replace('</head>','\n'.join(block)+'\n</head>',1)

def security_cleanup(s):
    def repl(m):
        tag=m.group(0)
        if re.search(r'\brel=',tag,re.I): return tag
        return tag[:-1]+' rel="noopener noreferrer">'
    return re.sub(r'<a\b[^>]*\btarget=["\']_blank["\'][^>]*>', repl, s, flags=re.I)

def process(p):
    fname=p.name
    if fname not in META: return
    s=p.read_text(encoding='utf-8',errors='ignore')
    s=clean_logo(s)
    if fname in LEGACY:
        s=re.sub(r'<ul class="nav-links">.*?</ul>',nav_for(fname),s,count=1,flags=re.S|re.I)
        s=re.sub(r'<style id="insiyab-global-polish">.*?</style>\s*','',s,flags=re.S|re.I)
        s=s.replace('</head>',POLISH+'\n</head>',1)
    if GA_ID not in s: s=s.replace('</head>',GA+'\n</head>',1)
    s=inject_meta(s,fname,*META[fname])
    s=security_cleanup(s)
    p.write_text(s,encoding='utf-8')

for f in ROOT.glob('*.html'): process(f)
urls=[]
for fname in META:
    loc=BASE+'/' if fname=='index.html' else f'{BASE}/{fname}'
    pr='1.0' if fname=='index.html' else ('0.3' if fname in {'privacy.html','terms.html'} else ('0.6' if fname.startswith('blog-') else '0.8'))
    freq='weekly' if fname in {'index.html','blog.html'} else 'monthly'
    urls.append(f'  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pr}</priority></url>')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(urls)+'\n</urlset>\n',encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n',encoding='utf-8')
print('InsiyabTech post-processing complete')
