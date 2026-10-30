import json,glob,sys,os
raw=sys.argv[1]
out=[]
for cik in ['0000034088','0000093410','0001163165','0000797468']:
    blocks=[json.load(open(f'{raw}/sub_{cik}.json'))['filings']['recent']]
    for f in glob.glob(f'{raw}/CIK{cik}-submissions-*.json'):
        blocks.append(json.load(open(f)))
    for b in blocks:
        for i,form in enumerate(b['form']):
            d=b['filingDate'][i]
            if form in ('DEF 14A','8-K') and '2003-06'<=d<='2020-12':
                if form=='8-K' and '5.07' not in b.get('items',['']*len(b['form']))[i]: continue
                out.append((cik,form,d,b['accessionNumber'][i],b['primaryDocument'][i],b.get('items',['']*99999)[i]))
out.sort()
for o in out: print('\t'.join(o))
