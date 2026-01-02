from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from memory import add_to_memory, get_recent_conversations  

# Initialize LLM
llm = ChatOllama(model="llama3.2")

# Prompt template
template = """
You are my assistant. Your name is Pulse. You control all of the other AIs. Eventually, you will
have access to my calendar and other apps. Some of the AIs that you will have access to are NEXUS, SHIELD, etc.

Here are some queries to answer: {queries}
""" 
prompt = ChatPromptTemplate.from_template(template)

# Function to extract only the text content from LLM responses
def extract_text(response) -> str:
    # LangChain AIMessage
    if hasattr(response, "content"):
        return response.content

    # Ollama raw dict
    if isinstance(response, dict):
        return response.get("response") or response.get("content") or ""

    # Fallback
    return str(response)

# Run LLM with memory integration
async def run_llm(queries: str) -> str:
    recent_memory = get_recent_conversations()
    formatted_prompt = f"{recent_memory}\n{prompt.format(queries=queries)}" if recent_memory else prompt.format(queries=queries)
    try:
        response = await llm.ainvoke(formatted_prompt)  # raw LLM response
        clean_response = extract_text(response)  # strip metadata
        if clean_response:
            add_to_memory(queries, clean_response)  # save only clean text
        return clean_response
    except asyncio.TimeoutError as e:
        print(f"Timeout error: {e}")
        return None
    except Exception as e:
        print(f"LLM error: {e}")
        return None

# Main interactive loop
async def main():
    print("Pulse is live. Type '/stop' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "/stop":
            print("Pulse: Goodbye.")
            break
        response = await run_llm(user_input)
        if response:
            print(f"Pulse: {response}\n")

# Optional test function
async def test_core():
    test_queries = [
        "Hello Pulse, how are you?",
        "Remember my favourite colour is blue",
        "My favourite day is Saturday",
        "Remember that I have an appointment on Wednesday at 9am @ London Tower"
    ]
    for query in test_queries:
        print(f"User: {query}")
        response = await run_llm(query)
        if response:
            print(f"Pulse: {response}\n")
        else:
            print("Pulse hasn't responded. Please try again later.\n")

print("Testing Core completed. Well done.")

# Run main loop
if __name__ == "__main__":
    asyncio.run(main())
