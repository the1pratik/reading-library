# Build the Gloss-style reading library -> library/index.html (+ items.json)
# Add items: append dicts to items_new.py NEW (source: Essay|Podcast|Newsletter|Instagram|X|Pick, added: YYYY-MM-DD), then: python3 build.py && cd library && git add -A && git commit -m update && git push
import json,hashlib
exec(open('items.py').read()); exec(open('items_new.py').read())
SRC={"Founder essays":"Essay","Tech essays":"Essay","Podcast notes":"Podcast"}
D=[]
for s,t,a,u,m,g,k,q in ITEMS: D.append(dict(source=SRC[s],title=t,author=a,url=u,minutes=m,tags=g,ideas=k,q=q,added="2026-10-12"))
D+=NEW
seen=set();out=[]
for d in D:
    if d['url'] in seen: continue
    seen.add(d['url']); d['id']=hashlib.md5(d['url'].encode()).hexdigest()[:8]; out.append(d)
json.dump(out,open('library/items.json','w'),indent=1)
html=open('template.html').read().replace('/*DATA*/[]',json.dumps(out,ensure_ascii=False).replace('</','<\\/'))
open('library/index.html','w').write(html)
print(len(out),'items')
