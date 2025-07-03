from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from my_agent.common.state import State

class MCPNode:
    def __init__(self):
        self.client = MultiServerMCPClient(
            {
                "math": {
                    "command": "python",
                    "args": ["/home/yuqi/langgraph/demo/my_agent/agents/mcp_agent/servers/mathMCP.py"],
                    "transport": "stdio",
                }
            }
        )

    async def create_agent(self):
        """
        Create the MCP agent with the necessary tools.
        """
        self.tools = await self.client.get_tools()
        self.agent = create_react_agent(
            tools=self.tools,
            model="gpt-4o",
        )

    def _convert_message_to_dict(self, message) -> dict:
        return {
            "role": message.type,
            "content": message.content
        }

    async def __call__(self, state: State) -> str:
        message = state["messages"]
        full_message = [{"role": "system", "content": "You are a helpful math assistant."}] + [
            self._convert_message_to_dict(msg) for msg in message
        ]
        response = await self.agent.ainvoke({
            "messages": full_message
        })
        return response