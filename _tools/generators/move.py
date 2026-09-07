import os,json,shutil,sys,time,csv
ROOT=os.getcwd(); DUMP=os.path.join(ROOT,'dump')
unused=json.load(open(os.path.expanduser('~/ocblog/unused.json')))
man=os.path.join(DUMP,'_moved-manifest.csv')
done=set()
if os.path.exists(man):
    with open(man,newline='',encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0]!='original_path': done.add(r[0])
budget=float(sys.argv[1]) if len(sys.argv)>1 else 100
t0=time.time(); moved=0; skipped=0; errs=[]
newf = not os.path.exists(man)
with open(man,'a',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    if newf: w.writerow(['original_path','moved_to','bytes'])
    for rel in unused:
        if rel in done: continue
        src=os.path.join(ROOT,rel.replace('/',os.sep))
        if not os.path.exists(src): skipped+=1; continue
        dst=os.path.join(DUMP,rel.replace('/',os.sep))
        os.makedirs(os.path.dirname(dst),exist_ok=True)
        if os.path.exists(dst):
            b,e=os.path.splitext(dst); n=1
            while os.path.exists('%s__%d%s'%(b,n,e)): n+=1
            dst='%s__%d%s'%(b,n,e)
        try:
            sz=os.path.getsize(src)
            shutil.move(src,dst)
            w.writerow([rel,os.path.relpath(dst,ROOT).replace(os.sep,'/'),sz]); moved+=1
        except Exception as ex:
            errs.append((rel,str(ex)[:90]))
            if len(errs)>8: break
        if time.time()-t0>budget: break
remaining=sum(1 for rel in unused if os.path.exists(os.path.join(ROOT,rel.replace('/',os.sep))))
print('moved this run: %d | already gone: %d | still to move: %d | %.1fs'%(moved,skipped,remaining,time.time()-t0))
if errs: print('ERRORS:',errs[:8])
