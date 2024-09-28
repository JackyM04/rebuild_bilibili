from email.quoprimime import unquote
import time
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Request, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
import httpx

# from routers.sound_api import router as sound_router
load_dotenv()
api_port = int(os.getenv("API_PORT", 8000))
        

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting up")
    yield

app = FastAPI(lifespan=lifespan)
# app.include_router(sound_router)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/get/recomvideo")
async def get(request: Request):
    headers = dict(request.headers)
    cookie = headers.get("uCookie","")
    #调试缓存机制
    try:
        with open("./testdb/recomvideo.txt", "r") as f:
            return json.load(f)
    except:
        pass
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(os.getenv("BILIBILI_RECOMVIDEO"), headers={
            "Content-Type": "application/json",
            "Authorization": f"{cookie}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        })
        with open("./testdb/recomvideo.txt", "w") as f:
            json.dump(response.json(), f)
        print(response.text)
        return response.json()

@app.post("/api/post/{url}")
async def post(url: str, headers: dict):
    httpx_client = httpx.AsyncClient()
    response = await httpx_client.post(url, headers=headers)
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=api_port)