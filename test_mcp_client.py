import subprocess
import sys
import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def main():
    # Start the MCP server in a separate process
    server_process = subprocess.Popen(
        [
            "uvx", 
            "mcp-server-motherduck", 
            "--db-path", 
            ":memory:", 
            "--result-format", 
            "markdown"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    
    # Configure server parameters to use the subprocess's pipes
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-motherduck", "--db-path", ":memory:", "--result-format", "markdown"],
        process=server_process  # You may need to adjust this based on your mcp version
    )
    
    try:
        # Give the server a moment to initialize
        await asyncio.sleep(2)
        
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("Calling query tool...", file=sys.stderr)
                result = await session.call_tool("query", {"query": "SELECT 42 AS answer"})
                print(f"Query result: {result}", file=sys.stderr)
                
                # Shut down the session
                await session.shutdown()
    finally:
        # Make sure to terminate the server process when done
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

if __name__ == "__main__":
    asyncio.run(main())