import sys,re,os
kw=re.compile(r'(climate|greenhouse|carbon|warming|renewable|emission|kyoto|co2|energy technology|planning assumptions|sequestration|geothermal)',re.I)
for f in sys.argv[1:]:
    T=re.sub(r'\s+',' ',open(f).read())
    ms=[m.start() for m in re.finditer(r'(submission of matters to a vote|5\.07 Submission)',T,re.I)]
    if not ms: print('=====',os.path.basename(f),'NO SECTION'); continue
    S=T[ms[-1]:ms[-1]+15000]
    print('=====',os.path.basename(f))
    for m in kw.finditer(S):
        pass
    out=[];last=-500
    for m in kw.finditer(S):
        if m.start()-last<250: continue
        last=m.start(); out.append(S[max(0,m.start()-120):m.start()+230])
    for o in out: print('   *',o)
