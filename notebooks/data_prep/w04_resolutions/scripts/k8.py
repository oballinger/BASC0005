import sys,re,os
kw=re.compile(r'(climate|greenhouse|carbon|methane|warming|degree|renewable|emission|reserve|lobbying|environmental expertise|dividend|oil sands|flaring|btu|energy|scenario|transition|petrochemical|sustainab)',re.I)
for f in sys.argv[1:]:
    T=re.sub(r'\s+',' ',open(f).read())
    i=T.find('5.07'); j=T.find('SIGNATURE',i); T=T[i:j if j>0 else None]
    segs=re.split(r'(?=\(\d{1,2}\) [A-Z]|(?<![\d,.]) \d{1,2}\. [A-Z]|STOCKHOLDER PROPOSAL|SHAREHOLDER PROPOSAL|Item \d+ ?[–—-])',T)
    print('=====',os.path.basename(f),'nseg',len(segs))
    for s in segs:
        if kw.search(s[:300]): print('  *',s[:420])
