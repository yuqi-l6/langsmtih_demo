from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from my_agent.agents.mcp_agent.agent import MCPAgent
from my_agent.agents.rag_agent.agent import RAGAgent

# Load MCPAgent and RAGAgent
# mcp_agent = MCPAgent()
rag_agent = RAGAgent()

# Create supervisor
supervisor = create_supervisor(
    agents=[rag_agent.create_workflow()],
    model=ChatOpenAI(model="gpt-4o"),
    prompt=(
        "You manage an MCP agent and a RAG agent. Assign work to them based on the input."
    )
).compile()

# # Example usage
# for chunk in supervisor.stream(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Perform math operations and retrieve relevant documents."
#             }
#         ]
#     }
# ):
#     print(chunk)
#     print("\n")