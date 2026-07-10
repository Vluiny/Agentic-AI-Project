from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from src.state import AgentState
from src.prompts.promptAI import SYSTEM_PROMPT_TOTAL
from dotenv import load_dotenv
from src.tools import info_search, time, get_weather
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm_fast = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.9,
    max_tokens=250,
)


tools = [time, info_search, get_weather]

ringan_react = create_react_agent(llm_fast, tools, prompt=SYSTEM_PROMPT_TOTAL)

# --- SATU NODE UTAMA ---
def tanya_ringan_node(state: AgentState):
    print("ringan diakses")
    hasil = ringan_react.invoke({"messages": state["messages"]})
    return {"messages": [hasil["messages"][-1]]}