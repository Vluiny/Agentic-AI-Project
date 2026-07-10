from langchain_core.messages import HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI

from dotenv import load_dotenv

load_dotenv()

llm_base_fast = ChatMistralAI(model="mistral-small-2506")

messages = [
    HumanMessage(content="hai"),
    AIMessage(content="halo"),
    HumanMessage(content="apakah anda bisa bahasa indonesia"),
    AIMessage(content="ya"),
    HumanMessage(content="saya sebelumnya bertanya apa?")
]

print(llm_base_fast.invoke(messages))