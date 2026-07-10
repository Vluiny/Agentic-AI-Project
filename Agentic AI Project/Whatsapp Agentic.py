from fastapi import FastAPI, Request
from langchain_core.messages import HumanMessage
from AgenticAI import app

import requests

WAHA_URL = "http://localhost:3000/api/sendText"

server = FastAPI()


@server.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    phone = data["payload"]["from"]
    text = data["payload"]["body"]

    config = {
        "configurable": {
            "thread_id": phone
        }
    }

    result = app.invoke(
        {
            "messages": [HumanMessage(content=text)]
        },
        config=config
    )

    reply = result["messages"][-1].content

    requests.post(
        WAHA_URL,
        json={
            "chatId": phone,
            "text": reply
        }
    )

    return {"ok": True}

    # print(json.dumps(data, indent=2, ensure_ascii=False))