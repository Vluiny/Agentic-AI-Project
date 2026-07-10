from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]