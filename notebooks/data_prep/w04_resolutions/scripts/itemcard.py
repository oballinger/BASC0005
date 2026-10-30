import sys,re,os
p=re.compile(r'\(?\s*items?\s+(\d+)\s+on\s+the\s+proxy',re.I)
for f in sys.argv[1:]:
    T=open(f).read(); L=[l.strip() for l in T.split('\n') if l.strip()]
    got={}
    for i,l in enumerate(L):
        m=p.search(l)
        if m and len(l)<160:
            n=int(m.group(1))
            if n in got: continue
            ctx=' '.join(L[max(0,i-3):i+1])
            got[n]=re.sub(r'(?i)stockholder proposals \((continued|concluded)\)','',ctx)[-200:]
    print('=====',os.path.basename(f))
    for n in sorted(got): print(f'  {n}: {got[n]}')
