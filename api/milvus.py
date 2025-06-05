import os
from pymilvus import connections,Collection

_host=os.getenv('MILVUS_HOST','localhost')
_port=os.getenv('MILVUS_PORT','19530')

connections.connect(host=_host,port=_port)


def get_col():
    return Collection('faces')


def search(vec,k=5):
    col=get_col()
    res=col.search([vec],'emb',{'metric_type':'L2','params':{'nprobe':10}},limit=k,output_fields=['meta'])
    out=[]
    for h in res[0]:
        m=h.entity.get('meta',{})
        out.append({'id':h.id,'dist':h.distance,'cam':m.get('cam'), 'ts':m.get('ts')})
    return out
