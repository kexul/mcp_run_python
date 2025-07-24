# Python Code Execution MCP Server

A Model Context Protocol (MCP) server allows AI assistants to execute Python code.

## Features

- **Python Code Execution**: Execute Python code with your installed python. **No sandbox!!!**. 
- **UTF-8 Encoding Support**: Proper handling of Unicode characters and encoding.

## Installation
1. Install dependencies in your python env:
   ```bash
   pip install fastmcp
   ```

2. Clone this repository.


## Usage

### Adding the Server to any chat client support mcp

```json
"python-interpreter": {
			"type": "stdio",
			"command": "path_to_your_python_exe",
			"args": [
				"path_to_the_server.py",
			]
		}
```

### Available Tools

#### `run_python_code`

Execute Python code and return detailed results.

**Parameters:**
- `code` (string): The Python code to execute

**Returns:**
- Execution status (success/failure)
- Return code
- Standard output
- Standard error
- Execution time

### Dependencies

- **fastmcp**: MCP server framework


## License

MIT

## Support

For issues and questions:
- Create an issue in the repository
- Check the FastMCP documentation for MCP-related questions

## Technical Notes

- The server runs Python code using the same interpreter that's running the server
- Working directory is preserved from the server's current directory
- Standard library modules are available by default
- Additional packages need to be installed in the server's Python environment