# Python Code Execution MCP Server

A Model Context Protocol (MCP) server that allows AI assistants to execute Python code with persistent state across multiple calls.

## Features

- **Python Code Execution**: Execute Python code with your installed Python interpreter. **No sandbox!!!**
- **Persistent State**: Variables and functions defined in previous executions remain available in subsequent calls
- **Environment Management**: Tools to reset environment and inspect defined variables

## Installation

1. Install dependencies in your Python environment:
```bash
pip install fastmcp
```

2. Clone this repository or download `server.py`.

## Usage

### Adding the Server to any MCP-compatible chat client

```json
{
"python-interpreter": {
	"type": "stdio",
	"command": "path_to_your_python_exe",
	"args": [
	"path_to_the_server.py"
	]
}
}
```

### Available Tools

#### `run_python_code`

Execute Python code and return detailed results. Variables and functions defined in previous executions will remain available in subsequent calls.

**Parameters:**
- `code` (string): The Python code to execute

**Returns:**
- Execution status (success/failure)
- Return code
- Standard output
- Standard error  
- Execution time

#### `reset_python_environment`

Reset the Python execution environment, clearing all variables and imports.

**Returns:**
- Confirmation message

#### `list_defined_variables`

List all currently defined variables and functions in the Python environment.

**Returns:**
- List of defined variables and functions with their types and values


### Dependencies

- **fastmcp**: MCP server framework
- **Python 3.6+**: Required for the server runtime

## Technical Notes

- **Persistent State**: Uses a global namespace to maintain variables and functions across executions
- **No Subprocess**: Executes code directly in the server process for better performance and state persistence
- **UTF-8 Support**: Handles Unicode characters properly without additional encoding setup
- **Error Handling**: Captures both stdout/stderr and Python exceptions with full stack traces
- **Working Directory**: Preserves the server's current working directory
- **Standard Library**: All standard library modules are available
- **Third-party Packages**: Additional packages must be installed in the server's Python environment

## Security Warning

⚠️ **This server executes arbitrary Python code without sandboxing. Only use in trusted environments.**

## License

MIT

## Support

For issues and questions:
- Create an issue in the repository
- Check the FastMCP documentation for MCP-related questions