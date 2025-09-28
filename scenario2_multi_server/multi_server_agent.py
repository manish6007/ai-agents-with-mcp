from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

def create_mcp_client(command, args):
    """Spins up an MCP server locally and returns a client."""
    client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command=command, args=args)
        )
    )
    return client

model = "anthropic.claude-3-sonnet-20240229-v1:0"
# Task for the agent
task = """
What is SageMaker's fine-tuning ability?
How can I fine-tune the Llama model?
What type of SageMaker instances will I need? How much do they cost?
Which region should I use?
Write the report.
"""

# 1. Create MCP clients for all required servers
doc_client = create_mcp_client("uvx", ["--from", 
            "awslabs.aws-documentation-mcp-server@latest", 
            "awslabs.aws-documentation-mcp-server.exe"])
pricing_client = create_mcp_client("uvx", ["--from", "awslabs.aws-pricing-mcp-server@latest", "awslabs.aws-pricing-mcp-server.exe"])

with doc_client, pricing_client:
    # 2. List tools from all MCP servers
    doc_tools = doc_client.list_tools_sync()
    pricing_tools = pricing_client.list_tools_sync()
    
    # 3. Combine all tools into a single list
    all_tools = doc_tools + pricing_tools 

    # 4. Create an agent with the combined tools
    agent = Agent(model=model, tools=all_tools)

    # 5. Use the agent to answer a complex question
    response = agent(task)
    print(response)

#Output will be like this:
"""
To answer your questions about SageMaker's fine-tuning capabilities and the costs involved, I will:

1. Search the AWS documentation for relevant information on SageMaker fine-tuning and the Llama model.
2. Retrieve pricing information for the recommended instance types across AWS regions.
3. Generate a detailed cost analysis report covering the key points.
Tool #1: search_documentation


The search results provide detailed information on SageMaker's fine-tuning capabilities for large language models like Llama:

- SageMaker supports fine-tuning pre-trained foundation models like Llama on custom datasets to improve performance on domain-specific tasks
- Fine-tuning optimizes model weights using prompt-response pairs, low-rank adapters, quantization aware training, and other advanced techniques
- There are multiple options to configure fine-tuning jobs - SageMaker Studio UI, SageMaker JumpStart, SageMaker Python SDK
- Users need to prepare their training data, upload it to S3, and specify instance types/hyperparameters for the fine-tuning job

To get pricing information for recommended instances:
Tool #2: get_pricing


The pricing query returned no results, likely because the specified instance types (g5.24xlarge, g5.48xlarge) are not valid SageMaker instance sizes. Let's try again following the recommendation to validate the instance types first:
Tool #3: get_pricing_attribute_values


The valid instance types seem to be:

- ml.g5.24xlarge 
- ml.g5.48xlarge
- ml.p3.16xlarge
- ml.p3.8xlarge

For fine-tuning large models like Llama, the recommended instances would likely be ml.g5.48xlarge or ml.p3.16xlarge based on having high GPU memory.

Let's get pricing for these across some common regions:
Tool #4: get_pricing


Based on the pricing data:

- ml.g5.48xlarge instances cost $20.36/hr in us-east-1 and us-west-2, and $22.73/hr in eu-west-1
- ml.p3.16xlarge instances cost $28.15/hr in us-east-1 and us-west-2, and $30.41/hr in eu-west-1

The ml.g5.48xlarge appears to be the more cost-effective option, especially in the us-east-1 and us-west-2 regions.

To fine-tune a large model like Llama, I would recommend using an ml.g5.48xlarge instance, likely in the us-east-1 region which has a good balance of performance, cost, and availability of AWS services.

Let me generate a detailed cost analysis report:
Tool #5: generate_cost_report


Oh it seems there was an error parsing the pricing data I provided. Let me try restructuring it:
Tool #6: generate_cost_report


# Cost Analysis for SageMaker Instance Usage

This cost analysis focuses on the Amazon SageMaker instance pricing for fine-tuning the LLaMA large language model. The key points covered are:

## Pricing Summary

- **ml.g5.48xlarge** instances cost:
    - $20.36 per hour in the us-east-1 and us-west-2 regions  
    - $22.73 per hour in the eu-west-1 region
- **ml.p3.16xlarge** instances cost: 
    - $28.15 per hour in the us-east-1 and us-west-2 regions
    - $30.41 per hour in the eu-west-1 region

The ml.g5.48xlarge offers better cost-performance, especially in the us-east-1 or us-west-2 regions.

## Assumptions

- Using 1 ml.g5.48xlarge instance for fine-tuning
- Fine-tuning job runs for 24 hours in the us-east-1 region
- Using the JupyterLab interface for model fine-tuning and monitoring

## Cost Estimates

With the assumptions above, the total cost for a 24-hour fine-tuning run on ml.g5.48xlarge in us-east-1 would be:

**24 hours x $20.36/hour = $488.64**

## Relative Costs

To provide context, here are the costs for alternative scenarios:

- 24 hours on ml.p3.16xlarge in us-east-1: **$675.36**
- 24 hours on ml.g5.48xlarge in eu-west-1: **$545.52**  
- 48 hours on ml.g5.48xlarge in us-east-1: **$977.28**

As you can see, using the recommended ml.g5.48xlarge instance in us-east-1 provides significant cost savings over other options.

## Limitations & Exclusions

This analysis does not cover:

- Data transfer costs between regions
- Storage costs for training data and model artifacts  
- Administration and monitoring overhead costs

The cost estimates provided focus solely on the SageMaker instance usage for the fine-tuning job itself.

## Conclusion

For cost-effective fine-tuning of large language models like LLaMA on Amazon SageMaker, the optimal choice is to use an **ml.g5.48xlarge instance in the us-east-1 region**. This configuration balances performance requirements with cost-efficiency, enabling 24-hour fine-tuning runs for an estimated $488.64.

As your requirements change, be sure to revisit this analysis and consider options like spot instances or reserved capacity to further optimize costs. Regularly monitoring and rightsizing resources based on actual usage is key to controlling spending.

# Cost Analysis for SageMaker Instance Usage

This cost analysis focuses on the Amazon SageMaker instance pricing for fine-tuning the LLaMA large language model. The key points covered are:

## Pricing Summary

- **ml.g5.48xlarge** instances cost:
    - $20.36 per hour in the us-east-1 and us-west-2 regions
    - $22.73 per hour in the eu-west-1 region
- **ml.p3.16xlarge** instances cost:
    - $28.15 per hour in the us-east-1 and us-west-2 regions
    - $30.41 per hour in the eu-west-1 region

The ml.g5.48xlarge offers better cost-performance, especially in the us-east-1 or us-west-2 regions.

## Assumptions

- Using 1 ml.g5.48xlarge instance for fine-tuning
- Fine-tuning job runs for 24 hours in the us-east-1 region
- Using the JupyterLab interface for model fine-tuning and monitoring

## Cost Estimates

With the assumptions above, the total cost for a 24-hour fine-tuning run on ml.g5.48xlarge in us-east-1 would be:

**24 hours x $20.36/hour = $488.64**

## Relative Costs

To provide context, here are the costs for alternative scenarios:

- 24 hours on ml.p3.16xlarge in us-east-1: **$675.36**
- 24 hours on ml.g5.48xlarge in eu-west-1: **$545.52**
- 48 hours on ml.g5.48xlarge in us-east-1: **$977.28**

As you can see, using the recommended ml.g5.48xlarge instance in us-east-1 provides significant cost savings over other options.

## Limitations & Exclusions

This analysis does not cover:

- Data transfer costs between regions
- Storage costs for training data and model artifacts
- Administration and monitoring overhead costs

The cost estimates provided focus solely on the SageMaker instance usage for the fine-tuning job itself.

## Conclusion

For cost-effective fine-tuning of large language models like LLaMA on Amazon SageMaker, the optimal choice is to use an **ml.g5.48xlarge instance in the us-east-1 region**. This configuration balances performance requirements with cost-efficiency, enabling 24-hour fine-tuning runs for an estimated $488.64.

As your requirements change, be sure to revisit this analysis and consider options like spot instances or reserved capacity to further optimize costs. Regularly monitoring and rightsizing resources based on actual usage is key to controlling spending.

"""