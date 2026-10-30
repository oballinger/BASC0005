import sys,re,os,csv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from us_master import R
raw=sys.argv[1]
num=re.compile(r'\d{1,3}(?:,\d{3}){2,}')
out=[]
for r in R:
    firm,yr,title,cat,status,bl,doc,ph,note=r
    For=Ag=None; ctx=''
    if doc and ph and status=='voted':
        T=re.sub(r'\s+',' ',open(f'{raw}/txt/{doc}.txt').read())
        ms=[m.start() for m in re.finditer(r'(submission of matters to a vote|5\.07)',T,re.I)]
        T=T[ms[-1] if 'Submission' in T or ms else 0:] if ms else T
        i=T.lower().find(ph.lower())
        if i<0: ctx='PHRASE NOT FOUND'
        else:
            ns=num.findall(T[i:i+700])
            if len(ns)>=2: For,Ag=[int(x.replace(',','')) for x in ns[:2]]
            ctx=T[i:i+260]
    sup=round(100*For/(For+Ag),1) if For else ''
    out.append(dict(firm=firm,year=yr,title=title,category=cat,status=status,borderline=bl,votes_for=For or '',votes_against=Ag or '',support_pct=sup,vote_doc=doc,note=note,ctx=ctx))
w=csv.DictWriter(sys.stdout,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
