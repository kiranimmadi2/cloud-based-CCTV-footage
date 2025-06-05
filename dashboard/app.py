from fastapi import FastAPI,WebSocket
from fastapi.staticfiles import StaticFiles

app=FastAPI()
app.mount('/',StaticFiles(directory='dashboard/static',html=True),name='static')
clients=[]

@app.websocket('/ws')
async def ws(ws:WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await ws.receive_text()
    except Exception:
        pass
    finally:
        clients.remove(ws)

async def broadcast(msg:dict):
    for c in clients:
        await c.send_json(msg)
