import os
import sys
import time
import io
import contextlib
import traceback
from fastmcp import FastMCP


mcp = FastMCP(name="Python Interpreter", 
              instructions="""
              This server provides python code interpreter with persistent state, 
              Call run_python_code() to run python code. Variables and functions 
              defined in previous executions will remain available.
              """)

# Global namespace for maintaining state across executions
global_namespace = {}


def execute_python_code_persistent(code: str, timeout: int = 10) -> dict:
    """Execute Python code in persistent global namespace"""
    
    # Prepare output capture
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    try:
        start_time = time.time()
        
        # Ensure code is UTF-8 encoded string
        if isinstance(code, bytes):
            code = code.decode('utf-8', errors='replace')
        
        # Set up output redirection
        with contextlib.redirect_stdout(stdout_capture), \
             contextlib.redirect_stderr(stderr_capture):
            
            # Execute code in global namespace
            exec(code, global_namespace)
        
        elapsed = time.time() - start_time
        stdout_content = stdout_capture.getvalue()
        stderr_content = stderr_capture.getvalue()
        
        return {
            'success': True,
            'returncode': 0,
            'stdout': stdout_content,
            'stderr': stderr_content,
            'elapsed': elapsed
        }
        
    except UnicodeDecodeError as e:
        elapsed = time.time() - start_time
        return {
            'success': False,
            'returncode': 1,
            'stdout': '',
            'stderr': f'Unicode decode error: {e}',
            'elapsed': elapsed
        }
    except Exception as e:
        elapsed = time.time() - start_time
        stderr_content = stderr_capture.getvalue()
        
        # Add exception info to stderr
        if stderr_content:
            stderr_content += "\n"
        stderr_content += f"Exception: {type(e).__name__}: {e}\n"
        stderr_content += traceback.format_exc()
        
        return {
            'success': False,
            'returncode': 1,
            'stdout': stdout_capture.getvalue(),
            'stderr': stderr_content,
            'elapsed': elapsed
        }
    finally:
        stdout_capture.close()
        stderr_capture.close()


@mcp.tool()
def run_python_code(code: str) -> str:
    """
    Execute Python code and return the result.
    Variables and functions defined in previous executions will remain available.
    """
    if not code.strip():
        return "Error: Code cannot be empty"
    
    result = execute_python_code_persistent(code, timeout=10)
    
    output = []
    
    if result['stdout']:
        output.append(f"{result['stdout']}")
    if result['stderr']:
        output.append(f"{result['stderr']}")
    
    return "\n".join(output)


@mcp.tool()
def reset_python_environment() -> str:
    """
    Reset the Python execution environment, clearing all variables and imports.
    """
    global global_namespace
    
    # Keep essential builtins
    builtins_to_keep = {
        '__builtins__': global_namespace.get('__builtins__', __builtins__)
    }
    
    global_namespace.clear()
    global_namespace.update(builtins_to_keep)
    
    return "Python environment has been reset. All variables and imports cleared."


@mcp.tool()
def list_defined_variables() -> str:
    """
    List all currently defined variables and functions in the Python environment.
    """
    if not global_namespace:
        return "No variables or functions are currently defined."
    
    output = ["=== Currently Defined Variables and Functions ===\n"]
    
    # Filter out built-in items
    user_items = {k: v for k, v in global_namespace.items() 
                  if not k.startswith('_')}
    
    if not user_items:
        return "No user-defined variables or functions are currently defined."
    
    for name, value in sorted(user_items.items()):
        try:
            if callable(value):
                if hasattr(value, '__name__'):
                    output.append(f"Function: {name}()")
                else:
                    output.append(f"Callable: {name}")
            else:
                value_type = type(value).__name__
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
                output.append(f"Variable: {name} ({value_type}) = {value_str}")
        except Exception as e:
            output.append(f"Variable: {name} (Error getting info: {e})")
    
    return "\n".join(output)



if __name__ == "__main__":
    mcp.run()