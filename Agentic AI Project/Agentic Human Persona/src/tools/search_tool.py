import os
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

info_search = TavilySearch(
    max_results=1,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    time_range="year",
    search_depth="advanced"
)