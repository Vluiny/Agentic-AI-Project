import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv() 

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

while True:
    if user_input := input("Masukkan pertanyaan Anda (atau ketik 'exit' untuk keluar): "):
        if user_input.lower() == "exit":
            break
    messages = [
        {
            "role": "user",
            "content": "" + user_input,
        },
    ]

    history = []  
    chat_response = client.chat.complete(
        model="mistral-small-2506",
        messages=messages + history,
    )

    print(chat_response.choices[0].message.content)
    history.append(chat_response.choices[0].message)
