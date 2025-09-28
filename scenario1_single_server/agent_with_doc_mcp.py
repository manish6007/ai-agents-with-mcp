from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=[
            "--from", 
            "awslabs.aws-documentation-mcp-server@latest", 
            "awslabs.aws-documentation-mcp-server.exe"
        ]
    )
))
model = "anthropic.claude-3-sonnet-20240229-v1:0"
# Create an agent with MCP tools
with stdio_mcp_client:
    # Get the tools from the MCP server
    tools = stdio_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(model=model, tools=tools)
    response = agent("What is AWS Lambda?")
    print(response)

#Output will be like this:
"""
Tool #1: search_documentation


The search results provide a good overview of what AWS Lambda is - a serverless compute service that allows running code (Lambda functions) in response to events or on a schedule, without needing to manage servers.

Some key points from the search result summaries:

- AWS Lambda enables running code for processing data streams, building backends, handling file uploads/database operations/scheduled tasks, etc. without provisioning servers.

- Lambda functions execute in response to events like HTTP requests, messages in queues, file uploads, scheduled times, etc.

- Lambda provides managed runtimes/execution environments for several programming languages like Node.js, Python, Java, C#, Go, etc.

- Lambda automatically scales the compute capacity based on incoming requests/events, and applies security patches automatically.

- AWS provides developer guides, API references, SDKs, and tools/libraries like PowerTools to build and manage Lambda functions.

To get a more detailed explanation, we can call 
Tool #2: read_documentation


The key details from the documentation overview:

- AWS Lambda is a serverless compute service that runs your code (Lambda functions) in response to events or on a schedule, without requiring you to provision or manage servers.

- With Lambda, you just upload your code and Lambda automatically runs it and scales the compute capacity up or down as needed based on incoming requests/events.

- Lambda supports several use cases like real-time stream processing, web applications, mobile backends, IoT backends, file processing, database operations, and scheduled/periodic tasks.    

- You organize your code into Lambda functions, control security/permissions through execution roles, and Lambda runs your functions using language-specific runtimes when triggered by events from AWS services.

- Key features include environment variables, versions, layers, code signing for security, concurrency/scaling controls, SnapStart for fast cold starts, response streaming, and container image support.

- Lambda integrates with VPC networks for private connectivity, and can invoke other AWS services or resources through configured permissions.

So in summary, AWS Lambda is a managed serverless compute platform that allows running code/applications without provisioning servers, automatically scaling, with pay-per-use pricing. Its event-driven model and seamless AWS service integration enables building a wide variety of real-time applications.

The key details from the documentation overview:

- AWS Lambda is a serverless compute service that runs your code (Lambda functions) in response to events or on a schedule, without requiring you to provision or manage servers.

- With Lambda, you just upload your code and Lambda automatically runs it and scales the compute capacity up or down as needed based on incoming requests/events.

- Lambda supports several use cases like real-time stream processing, web applications, mobile backends, IoT backends, file processing, database operations, and scheduled/periodic tasks.    

- You organize your code into Lambda functions, control security/permissions through execution roles, and Lambda runs your functions using language-specific runtimes when triggered by events from AWS services.

- Key features include environment variables, versions, layers, code signing for security, concurrency/scaling controls, SnapStart for fast cold starts, response streaming, and container image support.

- Lambda integrates with VPC networks for private connectivity, and can invoke other AWS services or resources through configured permissions.

So in summary, AWS Lambda is a managed serverless compute platform that allows running code/applications without provisioning servers, automatically scaling, with pay-per-use pricing. Its event-driven model and seamless AWS service integration enables building a wide variety of real-time applications.
"""
