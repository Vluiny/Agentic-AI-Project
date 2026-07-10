import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()
api_key = os.getenv("CEREBRAS_API_KEY")

client = Cerebras(api_key=api_key)

print("Mengirim prompt ke Cerebras... \n")

while True:
    history = [] 
    user_input = input("Masukkan pertanyaan Anda: ")
    if user_input.lower() == "exit":
        break
    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-oss-120b", 
        messages=history,
        temperature=0.7,
        max_tokens=1000
    )

    print("--- Hasil Response AI ---")
    print(response.choices[0].message.content)