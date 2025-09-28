from strands import Agent
from strands_tools import file_write, code_interpreter  # note: python_repl (not Python_ripple)

# Clear task and filename
task = "Write Python code that symbolically differentiates y = x**2 + 3*x + 5 and save it to diff.py"

model = "anthropic.claude-3-sonnet-20240229-v1:0"

# In the example the tools are provided as callables (decorated with @tool),
# so pass them directly (no instantiation) unless your local API requires otherwise.
tools = [ code_interpreter, file_write]

agent = Agent(model=model, tools=tools)

try:
    result = agent(task)
except Exception as e:
    print("Agent.run failed:", e)
else:
    print("Agent result:")
    print(result)


# Output should be something like:
"""
Here is how we can write Python code to symbolically differentiate y = x**2 + 3*x + 5 and save it to a file diff.py:
Tool #1: file_write
Do you want to proceed with the file write? [y/*] y


The key steps are:

1. Import the sympy module to do symbolic math
2. Create a symbolic variable x using sym.symbols('x') 
3. Define the symbolic expression y = x**2 + 3*x + 5
4. Use sym.diff(y, x) to take the derivative of y with respect to x
5. Print out the original function and its derivative

When you run diff.py, it will output:

Original function: y = x**2 + 3*x + 5  
Derivative: dy/dx = 2*x + 3

The differentiated expression dy/dx = 2*x + 3 is the symbolic derivative of the original function y = x**2 + 3*x + 5.Agent result:


The key steps are:

1. Import the sympy module to do symbolic math
2. Create a symbolic variable x using sym.symbols('x')
3. Define the symbolic expression y = x**2 + 3*x + 5
4. Use sym.diff(y, x) to take the derivative of y with respect to x
5. Print out the original function and its derivative

When you run diff.py, it will output:

Original function: y = x**2 + 3*x + 5
Derivative: dy/dx = 2*x + 3

The differentiated expression dy/dx = 2*x + 3 is the symbolic derivative of the original function y = x**2 + 3*x + 5.
"""