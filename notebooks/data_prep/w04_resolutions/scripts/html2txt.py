import sys,os,re,html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t in('p','div','br','tr','li','h1','h2','h3','h4','h5','td','table'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
        if t in('p','div','tr','li','h1','h2','h3','h4','h5','td'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
for src in sys.argv[2:]:
    raw=open(src,encoding='latin-1').read()
    if '<html' in raw.lower() or '<p' in raw.lower() or '<div' in raw.lower():
        p=P(); p.feed(raw); t=''.join(p.out)
    else: t=raw
    t=html.unescape(t).replace('\xa0',' ')
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    open(os.path.join(sys.argv[1],os.path.basename(src).rsplit('.',1)[0]+'.txt'),'w').write(t)
