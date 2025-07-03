from fastmcp import FastMCP


mcp = FastMCP("math")


@mcp.tool(name="add", description="Adds two numbers")
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@mcp.tool(name="multiply", description="Multiplies two numbers")
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool(name="divide", description="Divides two numbers")
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")