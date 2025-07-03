from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


system_prompt = """Be a helpful assistant"""
user_prompt = (
    "You are a helpful assistant tasked with answering complex questions by reasoning and retrieving relevant information from Wikipedia. "
    "**Your task:**\n"
    "(a) If no plan exists or a previous plan fails, analyze the question, formulate a new plan, and break it into sub-questions.\n"
    "(b) Try to answer each sub-question using reasoning over the current context.\n"
    "(c) If the available context is insufficient to answer a sub-question, generate a new search query using natural language and enclose it in <queries>...</queries>.\n"
    "(d) When new content is retrieved, review it carefully. Select relevant parts and highlight key information using <important>...</important> tags.\n"
    "    Example: <important>The driver Tom was born in New York.</important> means this content is likely useful for answering the original question.\n"
    "(e) Once enough information is gathered, produce a precise and concise answer to the original question and wrap it in <answer>...</answer>.\n\n"
    "**Guidelines:**\n"
    "- Search queries must be in **natural language**, concise, and include essential details (e.g., 'Who is the third highest paid Rangers F.C. player?'). Avoid keyword-only queries.\n"
    "- Use only **one** <queries>...</queries> tag per response.\n"
    "- If retrieved results are irrelevant, revise your query or plan accordingly.\n"
    "- All answers must be grounded in the provided or retrieved content. Do not rely on prior knowledge or hallucinate facts.\n"
    "- Reference to contexts wrapped in <important>...</important> tags help you answer the question.\n"
    "- Final answers must be brief, accurate, and directly address the question **using a few keywords**. The answer will be considered wrong if it has wrong format (e.g. a long sentence)! Example: Question: What's the capital of France? → <answer>Paris</answer>\n"

    "Question:\n{question}"
)
# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + [user_prompt.format(question=messages[-1].content)] + messages[:-1]
    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function to execute tools
tool_node = ToolNode(tools)