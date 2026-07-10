import json
import os
from fastapi import FastAPI, Request
from langchain_core.messages import HumanMessage
from AgenticAI import app
import requests
from dotenv import load_dotenv

load_dotenv()  #.env

WAHA_URL = "http://localhost:3000/api/sendText"

API_KEY = os.getenv("X_Api_Key")



server = FastAPI()

@server.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    event = data.get("event")
    if event != "message":
        print("Skip:", event)
        return {"ok": True}

    payload = data["payload"]
    phone = payload["from"]
    text = payload["body"]

    print("--- Incoming Message ---")
    print("Phone:", phone)
    print("Text:", text)
    print(json.dumps(data, indent=2, ensure_ascii=False))

    config = {
        "configurable": {
            "thread_id": phone
        }
    }

    result = await app.invoke(
        {
            "messages": [HumanMessage(content=text)]
        },
        config=config
    )
    
    print("--- Agent Result ---")
    print(result)

    reply = result["messages"][-1].content
    print("Reply:", reply)

    headers = {
        "X-Api-Key": API_KEY
    }

    res = requests.post(
        WAHA_URL,
        headers=headers,
        json={
            "session": "default",
            "chatId": phone,
            "text": reply
        }
    )

    print("--- WAHA Response ---")
    print("STATUS :", res.status_code)
    print("BODY   :", res.text)
    
    return {"status": "success"}