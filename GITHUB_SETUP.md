# Setting up mcp-server-motherduck from GitHub

This guide explains how to set up and use the mcp-server-motherduck directly from GitHub instead of using the pip package.

## Prerequisites

- `uv` installed, you can install it using `pip install uv` or `brew install uv`
- Git installed on your system

## Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yan-hic/mcp-server-motherduck.git
cd mcp-server-motherduck
```

## Setup with uv

Create a virtual environment and install dependencies using uv:

```bash
uv venv
uv pip install -e .
```

## Configuration for MCP Clients

When configuring your MCP clients (Cursor, VS Code, Claude Desktop), you'll need to modify the configuration to use the local repository instead of the pip package.

### Cursor Configuration

```json
{
  "mcpServers": {
    "mcp-server-motherduck": {
      "command": "uv",
      "args": [
        "--directory", 
        "/path/to/your/local/mcp-server-motherduck", 
        "run", 
        "mcp-server-motherduck", 
        "--db-path",
        "md:",
        "--motherduck-token",
        "<YOUR_MOTHERDUCK_TOKEN_HERE>"
      ]
    }
  }
}
```

### VS Code Configuration

Add to your User Settings (JSON) file:

```json
{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "motherduck_token",
        "description": "MotherDuck Token",
        "password": true
      }
    ],
    "servers": {
      "motherduck": {
        "command": "uv",
        "args": [
          "--directory", 
          "/path/to/your/local/mcp-server-motherduck", 
          "run", 
          "mcp-server-motherduck", 
          "--db-path",
          "md:",
          "--motherduck-token",
          "${input:motherduck_token}"
        ]
      }
    }
  }
}
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "mcp-server-motherduck": {
      "command": "uv",
      "args": [
        "--directory", 
        "/path/to/your/local/mcp-server-motherduck", 
        "run", 
        "mcp-server-motherduck", 
        "--db-path",
        "md:",
        "--motherduck-token",
        "<YOUR_MOTHERDUCK_TOKEN_HERE>"
      ]
    }
  }
}
```

## Testing the Server

You can test the server manually by running:

```bash
uv run mcp-server-motherduck --db-path md: --motherduck-token <your_motherduck_token>
```

For local DuckDB:

```bash
uv run mcp-server-motherduck --db-path /path/to/your/local.db
```

For in-memory database:

```bash
uv run mcp-server-motherduck --db-path :memory:
```

## Testing with a Client

You can test the MCP server with a simple Python client. Create a file called `test_mcp_client.py` with the following content:

```python
import json
import requests

# MCP server URL (default when running locally)
MCP_URL = "http://localhost:8080"

def query_mcp(sql_query):
    """Execute a SQL query on the MCP server."""
    payload = {
        "name": "query",
        "input": {
            "query": sql_query
        }
    }
    
    response = requests.post(f"{MCP_URL}/tools/execute", json=payload)
    return response.json()

def main():
    # Test with a simple query
    result = query_mcp("SELECT 'Hello, World!' AS greeting")
    print(json.dumps(result, indent=2))
    
    # Create a table and insert data
    query_mcp("CREATE TABLE test (id INTEGER, name VARCHAR)")
    query_mcp("INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie')")
    
    # Query the table
    result = query_mcp("SELECT * FROM test ORDER BY id")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

Run this script while the MCP server is running to test the functionality.
