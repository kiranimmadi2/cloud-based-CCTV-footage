import json,pygeohash,math,argparse
import networkx as nx

cams={'cam1':(12.9716,77.5946)}

def hav(p,q):
    R=6371000
    la1,lo1=p
    la2,lo2=q
    phi1=math.radians(la1)
    phi2=math.radians(la2)
    dphi=math.radians(la2-la1)
    dl=math.radians(lo2-lo1)
    a=math.sin(dphi/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2*R*math.atan2(math.sqrt(a),math.sqrt(1-a))

def build(dets):
    g=nx.Graph()
    for i,d in enumerate(dets):
        g.add_node(i,**d)
    n=len(dets)
    for i in range(n):
        for j in range(i+1,n):
            t1=dets[i]['ts'];t2=dets[j]['ts']
            if abs(t1-t2)>900:continue
            c1=cams.get(dets[i]['cam']);c2=cams.get(dets[j]['cam'])
            if not c1 or not c2:continue
            if hav(c1,c2)<=500:
                g.add_edge(i,j)
    comps=[sorted(c,key=lambda x:dets[x]['ts']) for c in nx.connected_components(g)]
    paths=[[{'cam':dets[i]['cam'],'ts':dets[i]['ts']} for i in c] for c in comps]
    return paths

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('file',nargs='?')
    ap.add_argument('--live',action='store_true')
    a=ap.parse_args()
    if a.live:
        return
    with open(a.file) as f:
        dets=json.load(f)
    print(json.dumps(build(dets)))

if __name__=='__main__':
    main()
