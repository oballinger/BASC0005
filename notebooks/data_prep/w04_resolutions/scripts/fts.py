import sys,json,urllib.request,urllib.parse,time
q,ciks,start,end=sys.argv[1:5]
p={'q':q,'dateRange':'custom','startdt':start,'enddt':end}
if ciks!='-': p['ciks']=ciks
import os
if os.environ.get('FORMS'): p['forms']=os.environ['FORMS']
u='https://efts.sec.gov/LATEST/search-index?'+urllib.parse.urlencode(p)
r=urllib.request.Request(u,headers={'User-Agent':'UCL teaching research o.ballinger@ucl.ac.uk'})
d=json.load(urllib.request.urlopen(r)); time.sleep(0.2)
print('total',d['hits']['total']['value'])
for h in d['hits']['hits'][:int(sys.argv[5]) if len(sys.argv)>5 else 15]:
    s=h['_source']; print(s['file_date'],s['form'],h['_id'],s.get('file_description'),s['display_names'][0][:30])
