from mcp.server import FastMCP

mcp = FastMCP("Calculator Server")

@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:
    """Add two numbers and return the result."""
    return x + y

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divides the first number by the second."""
    return a / b

mcp.run(transport="streamable-http")

#Output will be like this:
"""
(ai-agents-with-mcp) C:\git\ai-agents-with-mcp>python scenario3_custom_server\calculator_server.py
INFO:     Started server process [18496]
INFO:     Waiting for application startup.
[09/28/25 13:19:46] INFO     StreamableHTTP session manager      streamable_http_manager.py:110
                             started                                                           
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:43984 - "POST /mcp/ HTTP/1.1" 307 Temporary Redirect
[09/28/25 13:20:18] INFO     Created new transport with session  streamable_http_manager.py:233
                             ID:                                                               
                             d5acecf0e98848c78c39ee7b9edc24ee                                  
INFO:     127.0.0.1:43984 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:43985 - "POST /mcp/ HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:43986 - "GET /mcp/ HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:43985 - "POST /mcp HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:43986 - "GET /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:43987 - "POST /mcp/ HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:43987 - "POST /mcp HTTP/1.1" 200 OK
                    INFO     Processing request of type ListToolsRequest          server.py:664
INFO:     127.0.0.1:43991 - "POST /mcp/ HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:43991 - "POST /mcp HTTP/1.1" 200 OK
"""