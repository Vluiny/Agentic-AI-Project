import os
from dotenv import load_dotenv
from openai import OpenAI
import os
from ollama import Client


load_dotenv()
api_key = os.getenv("OLLAMA_API_KEY")

client = Client(
host="https://ollama.com",
headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

print("Mengirim request ke Ollama Cloud... \n")

history = []
while True:
    user_input = input("Masukkan pertanyaan Anda: \n")
    history.append({"role": "user", "content": user_input})
    if user_input.lower() == "exit":
        break
    messages = [
    {
        'role': 'user',
        'content': user_input
    },
    ]

    for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True, )