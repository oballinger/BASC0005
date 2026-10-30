import json,glob,sys,re
raw=sys.argv[1]
for cik,months in [('0000313807',('03','04','05')),('0001306965',('03','04','05','06'))]:
    bl=[json.load(open(f'{raw}/sub_{cik}.json'))['filings']['recent']]+[json.load(open(f)) for f in glob.glob(f'{raw}/CIK{cik}-submissions-*.json')]
    for b in bl:
        for i,fm in enumerate(b['form']):
            d=b['filingDate'][i]
            if fm.startswith('6-K') and '2004'<=d[:4]<='2019' and d[5:7] in months:
                print(cik,d,b['accessionNumber'][i],b['primaryDocument'][i],b['primaryDocDescription'][i][:60],sep='\t')
