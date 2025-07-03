from typing import TypedDict, Literal
import asyncio
from langgraph.graph import StateGraph, add_messages
from my_agent.common.state import State
from my_agent.agents.mcp_agent.nodes.MCP_node import MCPNode

class GraphConfig(TypedDict):
    model_name: Literal["openai"]

class MCPAgent:
    """
    MCP Agent that interacts with a Multi-Server MCP Client to perform math operations.
    """

    def __init__(self):
        self.model_name = "gpt-4o"
        self.prompt_path = "/home/yuqi/langgraph/demo/my_agent/agents/mcp_agent/prompts/mcp_prompt.txt"

    async def create_workflow(self) -> StateGraph:
        """
        Create the workflow for the MCP Agent.
        """
        mcp_node = MCPNode()

        await mcp_node.create_agent()

        workflow = StateGraph(State, config_schema=GraphConfig)

        workflow.add_sequence(
            [
                "mcp_node", mcp_node
            ]
        )

        workflow.set_entry_point("mcp_node")

        graph = workflow.compile()

        return graph

