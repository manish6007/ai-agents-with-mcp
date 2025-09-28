from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient

def create_streamable_http_transport():
    return streamablehttp_client("http://127.0.0.1:8000/mcp/")

streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
model = "anthropic.claude-3-sonnet-20240229-v1:0"
with streamable_http_mcp_client:
    # Get tools exposed by the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()
    # Add these tools to an Agent
    agent = Agent(model=model,tools=tools)
    print(agent("add 2 and 3 subtract from 100 mutilply with 87 devide by 67"))  # Should output: 5

#Output will be like this:
"""
Here are the steps to perform that calculation:
Tool #1: add

Tool #2: subtract

Tool #3: multiply

Tool #4: divide


So, the result of adding 2 and 3, subtracting that from 100, multiplying by 87, and then dividing by 67 is 123.36.

So, the result of adding 2 and 3, subtracting that from 100, multiplying by 87, and then dividing by 67 is 123.36.

"""