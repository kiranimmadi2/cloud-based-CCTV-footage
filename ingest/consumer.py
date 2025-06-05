import json,pygeohash,datetime
from confluent_kafka import Consumer
from pymilvus import connections,FieldSchema,CollectionSchema,DataType,Collection

cams={'cam1':(12.9716,77.5946)}

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'ingest','auto.offset.reset':'earliest'})
c.subscribe(['faces.raw'])
connections.connect()

fields=[FieldSchema(name='emb',dtype=DataType.FLOAT_VECTOR,dim=512),FieldSchema(name='meta',dtype=DataType.JSON)]
col=None
if 'faces' in Collection.list_collections():
    col=Collection('faces')
else:
    schema=CollectionSchema(fields,description='faces')
    col=Collection('faces',schema)
    col.create_index('emb',{'index_type':'IVF_FLAT','metric_type':'L2','params':{'nlist':1024}})
    col.load()

while True:
    msg=c.poll(1.0)
    if not msg or msg.error():
        continue
    data=json.loads(msg.value())
    ts=datetime.datetime.utcnow().isoformat()
    lat,lon=cams.get(data['cam_id'],(0,0))
    gh=pygeohash.encode(lat,lon)
    embs=data['embeddings']
    metas=[{'cam':data['cam_id'],'ts':ts,'geohash':gh} for _ in embs]
    col.insert([embs,metas])
