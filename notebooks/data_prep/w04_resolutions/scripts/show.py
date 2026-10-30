import sys,re
# usage: show.py file phrase nchars
f,ph,n=sys.argv[1],sys.argv[2],int(sys.argv[3])
T=re.sub(r'\s+',' ',open(f).read())
idx=[m.start() for m in re.finditer(re.escape(ph),T,re.I)]
# choose occurrence followed by 'submitted'/'notified'/'resolved' within 1500 chars
best=None
for i in idx:
    w=T[i:i+600].lower()
    if any(k in w for k in ('submitted by','notified','proponent','advised','filed by','intends to present','owner of')): best=i; break
if best is None and idx: best=idx[-1]
if best is None: print('NOT FOUND'); sys.exit()
w=T[best:best+6000]; r=re.search(r'(be it resolved|resolved)',w,re.I)
print('HEAD:',w[:200]); print('RES:',w[r.start():r.start()+n] if r else 'no resolved')
