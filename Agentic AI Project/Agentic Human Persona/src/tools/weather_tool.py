# src/tools/weather_tool.py
import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Mengambil data cuaca real-time untuk kota tertentu di Indonesia atau global."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            kondisi = data["weather"][0]["description"]
            suhu = data["main"]["temp"]
            kelembapan = data["main"]["humidity"]
            return f"Cuaca di {city}: {kondisi.capitalize()}, Suhu: {suhu}°C, Kelembapan: {kelembapan}%."
        return f"Gagal mengambil data cuaca untuk {city}. Kode status: {response.status_code}"
    except Exception as e:
        return f"Error saat menghubungi API cuaca: {str(e)}"