import os
import time
import requests
from dotenv import load_dotenv

# langchain_core / langchain_openai / langgraph imports
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END

# Load .env
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY")
BRIGHTDATA_SERP_ZONE = os.getenv("BRIGHTDATA_SERP_ZONE")
BRIGHTDATA_GPT_DATASET_ID = os.getenv("BRIGHTDATA_GPT_DATASET_ID")
BRIGHTDATA_PREPLEXITY_DATASET_ID = os.getenv("BRIGHTDATA_PREPLEXITY_DATASET_ID")

# Basic validation / debug
print("Loaded OPENAI_API_KEY:", (OPENAI_API_KEY[:10] + "..." ) if OPENAI_API_KEY else None)
print("Loaded BRIGHTDATA_API_KEY:", (BRIGHTDATA_API_KEY[:10] + "..." ) if BRIGHTDATA_API_KEY else None)
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment (.env).")

# BrightData headers (safe if key is None)
Headers = {
    "Authorization": f"Bearer {BRIGHTDATA_API_KEY}" if BRIGHTDATA_API_KEY else "",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# ------------------ HELPERS ------------------ #
def safe_post_json(url, headers=None, json_payload=None, timeout=30):
    """Wrapper around requests.post returning JSON or {} on error."""
    try:
        r = requests.post(url, headers=headers or {}, json=json_payload or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[safe_post_json] request failed: {e} (url={url})")
        return {}

def safe_get_json(url, headers=None, timeout=30):
    """Wrapper around requests.get returning JSON or {} on error."""
    try:
        r = requests.get(url, headers=headers or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[safe_get_json] request failed: {e} (url={url})")
        return {}

def extract_agent_answer(result):
    """
    Try multiple ways to extract final text from agent responses.
    Returns a string.
    """
    # dict-like with ['messages'] where each message has .content or ['content']
    try:
        if isinstance(result, dict) and "messages" in result:
            msgs = result["messages"]
            if msgs:
                m = msgs[-1]
                # m might be dict or object
                if isinstance(m, dict) and "content" in m:
                    return m["content"]
                if hasattr(m, "content"):
                    return m.content
        # object with .messages attribute
        if hasattr(result, "messages"):
            msgs = result.messages
            if msgs:
                m = msgs[-1]
                if hasattr(m, "content"):
                    return m.content
                if isinstance(m, dict) and "content" in m:
                    return m["content"]
        # maybe it's an AIMessage-like object (single)
        if hasattr(result, "content"):
            return result.content
        # fallback: string or list
        if isinstance(result, (list, tuple)):
            return str(result[-1])
        return str(result)
    except Exception as e:
        print(f"[extract_agent_answer] failed to extract: {e}")
        return str(result)

# ------------------ SEARCH TOOLS ------------------ #

@tool(description="search using google")
def google_search(query: str) -> str:
    print("[tool] Google search:", query)
    payload = {
        "zone": BRIGHTDATA_SERP_ZONE,
        "url": f"https://google.com/search?q={requests.utils.quote(query)}&brd_json=1",
        "format": "raw",
    }
    data = safe_post_json("https://api.brightdata.com/requests?async=true", headers=Headers, json_payload=payload)
    organic = data.get("organic") or []
    if not isinstance(organic, list):
        organic = []
    result = []
    for item in organic:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("description", "")
        result.append(f"{title}\nLink: {link}\nSnippet: {snippet}")
    return "\n\n".join(result)[:10000]

@tool(description="search using bing")
def bing_search(query: str) -> str:
    print("[tool] Bing search:", query)
    payload = {
        "zone": BRIGHTDATA_SERP_ZONE,
        "url": f"https://bing.com/search?q={requests.utils.quote(query)}&brd_json=1",
        "format": "raw",
    }
    data = safe_post_json("https://api.brightdata.com/requests?async=true", headers=Headers, json_payload=payload)
    organic = data.get("organic") or []
    if not isinstance(organic, list):
        organic = []
    result = []
    for item in organic:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("description", "")
        result.append(f"{title}\nLink: {link}\nSnippet: {snippet}")
    return "\n\n".join(result)[:10000]

@tool(description="search using reddit")
def reddit_search(query: str) -> str:
    print("[tool] Reddit search:", query)
    full_q = "site:reddit.com " + (query or "")
    payload = {
        "zone": BRIGHTDATA_SERP_ZONE,
        "url": f"https://google.com/search?q={requests.utils.quote(full_q)}&brd_json=1",
        "format": "raw",
    }
    data = safe_post_json("https://api.brightdata.com/requests?async=true", headers=Headers, json_payload=payload)
    organic = data.get("organic") or []
    if not isinstance(organic, list):
        organic = []
    result = []
    for item in organic:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("description", "")
        result.append(f"{title}\nLink: {link}\nSnippet: {snippet}")
    return "\n\n".join(result)[:10000]

@tool(description="search using x")
def X_search(query: str) -> str:
    print("[tool] X search:", query)
    full_q = "site:x.com " + (query or "")
    payload = {
        "zone": BRIGHTDATA_SERP_ZONE,
        "url": f"https://google.com/search?q={requests.utils.quote(full_q)}&brd_json=1",
        "format": "raw",
    }
    data = safe_post_json("https://api.brightdata.com/requests?async=true", headers=Headers, json_payload=payload)
    organic = data.get("organic") or []
    if not isinstance(organic, list):
        organic = []
    result = []
    for item in organic:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("description", "")
        result.append(f"{title}\nLink: {link}\nSnippet: {snippet}")
    return "\n\n".join(result)[:10000]

# ------------------ AI TOOLS (BrightData dataset triggers) ------------------ #

def _trigger_brightdata_dataset(dataset_id: str, prompt: str) -> dict:
    """Trigger a BrightData dataset and wait for snapshot. Returns snapshot item (dict) or {}."""
    if not BRIGHTDATA_API_KEY or not dataset_id:
        print("[_trigger_brightdata_dataset] BrightData API key or dataset_id missing.")
        return {}
    payload = {"url": "https://unused", "prompt": prompt}
    url = f"https://api.brightdata.com/datasets/v3/trigger?dataset_id={dataset_id}&format=json&custom_output_fields=answer"
    resp = safe_post_json(url, headers=Headers, json_payload=payload)
    snapshot_id = resp.get("snapshot_id")
    if not snapshot_id:
        print("[_trigger_brightdata_dataset] no snapshot_id in response.")
        return {}
    # wait
    for _ in range(60):  # up to ~5 minutes (60 * 5s)
        status = safe_get_json(f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}", headers=Headers)
        if status.get("status") == "ready":
            break
        time.sleep(5)
    snapshots = safe_get_json(f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json", headers=Headers)
    if isinstance(snapshots, list) and snapshots:
        return snapshots[0]
    return {}

@tool(description="use chatgpt to answer questions with sources")
def gpt_prompt(query):
    print("ChatGPT tool is being used------------")
    payload = {"url": "https://chatgpt.com", "prompt": query}
    url = f"https://api.brightdata.com/datasets/v3/trigger?dataset_id={BRIGHTDATA_GPT_DATASET_ID}&format=json&custom_output_fields=answer"
    response = requests.post(url, headers=Headers, json=payload)
    snapshot_id = response.json().get("snapshot_id")
    
    while True:
        status = requests.get(f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}", headers=Headers).json()
        if status.get("status") == "ready":
            break
        time.sleep(5)
    
    data = requests.get(f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json", headers=Headers).json()[0]
    answer = data.get("answer_text_markdown", [{}])[0].get("text", "No answer found")
    sources = data.get("sources", [])
    
    # Format sources nicely
    sources_text = "\n".join([f"{src.get('title','')} - {src.get('url','')}" for src in sources])
    
    return {"answer": answer, "sources": sources_text}


@tool(description="use perplexity to answer questions via BrightData dataset")
def get_preplexity_prompt(query: str) -> str:
    print("[tool] preplexity via BrightData:", query)
    data = _trigger_brightdata_dataset(BRIGHTDATA_PREPLEXITY_DATASET_ID, query)
    try:
        text = data.get("answer_text_markdown", [{}])[0].get("text") if data else None
    except Exception:
        text = None
    sources = data.get("sources", "") if data else ""
    if not text:
        text = data.get("answer", "") or data.get("text", "") or "No answer found"
    return text + ("\n\nSources:\n" + str(sources) if sources else "")

# ------------------ AGENT SETUP ------------------ #

# Explicitly pass API key to ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)

# create_react_agent: supply model and the decorated tool functions
agent = create_react_agent(
    model=llm,
    tools=[google_search, bing_search, reddit_search, X_search, gpt_prompt, get_preplexity_prompt],
    debug=False,
    prompt = (
    "You are a smart search assistant. Use the following tools to answer the user's question. "
    "If you use a tool, only use the information from the tool to construct your final answer. "
    "If you do not know the answer, clearly say you don't know. Do not make up information.\n\n"
    "{tools}\n\n"
    "Answer format (like Google search result with sources):\n"
    "Question: the input question\n"
    "Thought: your reasoning process\n"
    "Action: select one of [{tool_names}] to find information\n"
    "Action Input: what you will search\n"
    "Observation: the result from the tool\n"
    "... (repeat Thought/Action/Action Input/Observation as needed)\n"
    "Thought: I now know the final answer\n"
    "Final Answer: provide a concise, factual answer\n"
    "Sources: list the URLs or references from the tools you used\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "{agent_scratchpad}"
)

)

def agent_node(state: dict) -> dict:
    """
    Node function for the StateGraph. Uses HumanMessage for the agent input.
    """
    # create a proper message object
    user_msg = HumanMessage(content=state.get("query", ""))
    # invoke the agent
    result = agent.invoke({"messages": [("human", state["query"])]})
    # robustly extract the answer
    answer = extract_agent_answer(result)
    state["answer"] = result["messages"][-1].content
    return state

# ------------------ GRAPH ------------------ #
graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.add_edge("agent", END)
graph.set_entry_point("agent")
apps = graph.compile()

# ------------------ RUN ------------------ #
if __name__ == "__main__":
    q = input("query> ").strip()
    if not q:
        print("No query provided.")
    else:
        out = apps.invoke({"query": q})
        # out is normally a dict with 'answer' key (we set it in agent_node)
        print("Result:", out.get("answer") if isinstance(out, dict) else out)
