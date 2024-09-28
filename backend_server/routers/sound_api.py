import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from dotenv import load_dotenv
import os

from fastapi.responses import FileResponse
from dependencies import bili_ins as bi
import asyncio
from bili_ws.ws import BiliClient

router = APIRouter()
load_dotenv()

@router.websocket("/ws/ws/{idCode}")
async def websocket_endpoint(websocket: WebSocket, idCode:str):
    await websocket.accept()
    if idCode not in bi.instances:
        await websocket.send_json({"status":"error","msg":"idCode not found"})
        await websocket.close()
        return
    task_send_task = asyncio.create_task(send_task(websocket,idCode))
    task_recv_task = asyncio.create_task(recv_task(websocket))
    done, pending = await asyncio.wait([task_send_task, task_recv_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

async def send_task(websocket: WebSocket,idCode:str):
    cli:BiliClient = bi.instances[idCode]
    msg_hooker = cli.msg_hooker
    msg = cli.msg
    try:
        async with cli:
            asyncio.create_task(cli.run())
            while websocket.client_state !=2:
                print("等待消息")
                async with msg_hooker:
                    await msg_hooker.wait()
                    await websocket.send_json(msg)
                    print(msg)
                
    except Exception as e:
        print(e)
    finally:
        print("send_task end")
        

async def recv_task(websocket: WebSocket):
    try:
        while websocket.client_state !=2:
            data = await websocket.receive_json()
            print(data)
    except Exception as e:
        print(e)
    finally:
        print("recv_task end")

@router.get("/api/get_funcard/{idCode}")
async def get_funcard(idCode:str):
    if idCode not in bi.instances:
        return {"status":"error","msg":"idCode not found"}
    
    with open("./db/functionCard.json","r") as f:
        funcard = f.read()
        funcard = json.loads(funcard)
    return {"status":"success","functionCard":funcard["functionCardList"]}

@router.get("/api/get_audio")
async def get_audio(file: str):
    file_path = f"./db/audiofile/{file}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="audio/mpeg")

@router.websocket("/ws/streamuiws/{idCode}")
async def websocket_endpoint(websocket: WebSocket, idCode:str):
    await websocket.accept()
    if idCode not in bi.instances:
        print(idCode,bi.instances)
        await websocket.send_json({"status":"error","msg":"idCode not found"})
        await websocket.close()
        return
    task_send_task = asyncio.create_task(streamui_send_task(websocket,idCode))
    task_recv_task = asyncio.create_task(recv_task(websocket))
    done, pending = await asyncio.wait([task_send_task, task_recv_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

async def streamui_send_task(websocket: WebSocket,idCode:str):
    cli:BiliClient = bi.instances[idCode]
    msg_hooker = cli.msg_hooker
    msg = cli.msg
    try:
        while websocket.client_state !=2:
            print("等待消息")
            async with msg_hooker:
                await msg_hooker.wait()
                await websocket.send_json(msg)
                print(msg)
            
    except Exception as e:
        print(e)
    finally:
        print("send_task end")

@router.post("/api/set_userConfig/{idCode}")
async def set_userConfig(idCode:str,config:dict):
    if idCode not in bi.instances:
        return {"status":"error","msg":"idCode not found"}
    cli:BiliClient = bi.instances[idCode]
    cli.userConfig = config
    print(config)
    return {"status":"success"}

@router.get("/api/get_userConfig/{idCode}")
async def get_userConfig(idCode:str):
    if idCode not in bi.instances:
        return {"status":"error","msg":"idCode not found"}
    cli:BiliClient = bi.instances[idCode]
    print(cli.userConfig)
    return {"status":"success","userConfig":cli.userConfig}
