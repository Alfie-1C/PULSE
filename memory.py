import json
from pathlib import Path

MEMORY_FILE = Path("pulse_memory.json")
DEFAULT_MEMORY = {"conversations": []}

def load_memory() -> dict:
    """
    Load memory from file. If file is missing or corrupted, reset to default.
    """
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Memory file corrupted. Resetting memory.")
            save_memory(DEFAULT_MEMORY)
            return DEFAULT_MEMORY.copy()
    # File doesn't exist → create it
    save_memory(DEFAULT_MEMORY)
    return DEFAULT_MEMORY.copy()

def save_memory(memory: dict):
    """
    Save memory to file in clean JSON format.
    """
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

def normalize_response(assistant_response) -> str:
    
    #Convert assistant_response to plain string if it's an object (e.g., AIMessage)
    
    if isinstance(assistant_response, str):
        return assistant_response
    try:
        return assistant_response.content
    except AttributeError:
        return str(assistant_response)

def add_to_memory(user_input: str, assistant_response):
   
   # Add a new conversation entry to memory.
    #Converts LLM objects to plain strings before storing.
   
    memory = load_memory()
    assistant_response = normalize_response(assistant_response)

    memory.setdefault("conversations", [])
    memory["conversations"].append({
        "user": user_input,
        "assistant": assistant_response
    })

    # Keep only the last 10 conversations
    memory["conversations"] = memory["conversations"][-10:]
    save_memory(memory)

def get_recent_conversations(n: int = 5) -> str:
    """
    Retrieve the last n conversations as a formatted string.
    """
    memory = load_memory()
    recent = memory.get("conversations", [])[-n:]
    return "\n".join([f"User: {c['user']}\nPulse: {c['assistant']}" for c in recent])
