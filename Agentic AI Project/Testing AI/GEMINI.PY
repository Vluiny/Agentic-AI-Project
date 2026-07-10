import os
from google import genai
from dotenv import load_dotenv

load_dotenv() 

client = genai.Client()

chat = client.chats.create(model="gemini-3.1-flash-lite")

while True:
    try:
        user_input = input("Anda: ")
        
        if user_input.lower() in ['keluar', 'exit', 'quit']:
            print("Sampai jumpa!")
            break
            
        if not user_input.strip():
            continue

        response = chat.send_message(user_input)
        
        print(f"\nGemini: {response.text}\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        break
