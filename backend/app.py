from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid

# LangGraph
from langgraph.graph import StateGraph, END

# APP 
app = FastAPI()

# ✅ CORS (IMPORTANT for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE 
db = {"interactions": {}}

# SCHEMA
class ChatInput(BaseModel):
    message: str

class Interaction(BaseModel):
    hcp_name: str
    notes: str
    products: Optional[List[str]] = []
    follow_up: Optional[str] = None

#  TOOLS 

def log_tool(state):
    text = state["input"]

    interaction_id = str(uuid.uuid4())

    db["interactions"][interaction_id] = {
        "id": interaction_id,
        "text": text,
        "ai": "AI summary (mocked)"
    }

    return {"output": f"✅ Logged Interaction ID: {interaction_id}"}


def edit_tool(state):
    return {"output": "✏️ Interaction edited successfully"}


def insight_tool(state):
    interactions = list(db["interactions"].values())

    if not interactions:
        return {"output": "📊 No interactions available"}

    return {
        "output": f"📊 Total interactions: {len(interactions)}. HCP engagement looks consistent."
    }


def suggest_tool(state):
    return {
        "output": "💡 Suggested Action: Follow up with the HCP in 3 days."
    }


def followup_tool(state):
    return {"output": "📅 Follow-up scheduled successfully"}

# ROUTER 

def router(state):
    msg = state["input"].lower()

    if "edit" in msg:
        return "edit"
    elif "insight" in msg:
        return "insight"
    elif "suggest" in msg:
        return "suggest"
    elif "follow" in msg:
        return "follow"
    else:
        return "log"

# LANGGRAPH

graph_builder = StateGraph(dict)

graph_builder.add_node("log", log_tool)
graph_builder.add_node("edit", edit_tool)
graph_builder.add_node("insight", insight_tool)
graph_builder.add_node("suggest", suggest_tool)
graph_builder.add_node("follow", followup_tool)

graph_builder.set_conditional_entry_point(router)

graph_builder.add_edge("log", END)
graph_builder.add_edge("edit", END)
graph_builder.add_edge("insight", END)
graph_builder.add_edge("suggest", END)
graph_builder.add_edge("follow", END)

graph = graph_builder.compile()

# API 

@app.get("/")
def home():
    return {"msg": "CRM Backend Running"}

@app.post("/chat")
def chat(input: ChatInput):
    try:
        result = graph.invoke({"input": input.message})
        return {"response": result["output"]}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

@app.post("/form")
def form(data: Interaction):
    interaction_id = str(uuid.uuid4())
    db["interactions"][interaction_id] = data.dict()
    return {"msg": "Saved", "id": interaction_id}

@app.get("/all")
def all_data():
    return db