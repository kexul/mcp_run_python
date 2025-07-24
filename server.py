import os
import sys
import subprocess
import time
from fastmcp import FastMCP


mcp = FastMCP(name="Python Interpreter", 
              instructions="""
              This server provides python code interpreter, 
              Call execute_python_code() to run python code. 
              """)


def execute_python_code(code: str, timeout: int = 10) -> dict:
    python_path = sys.executable
    
    code_with_encoding = f"# -*- coding: utf-8 -*-\n{code}"
    
    try:
        start_time = time.time()
        
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'  
        
        process = subprocess.Popen(
            [python_path, "-u"],  
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',  
            cwd=os.getcwd(),
            env=env
        )
        
        stdout, stderr = process.communicate(input=code_with_encoding, timeout=timeout)
        elapsed = time.time() - start_time
        
        return {
            'success': process.returncode == 0,
            'returncode': process.returncode,
            'stdout': stdout,
            'stderr': stderr,
            'elapsed': elapsed
        }
        
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'success': False,
            'returncode': -1,
            'stdout': '',
            'stderr': f'Timeout（{timeout}s）',
            'elapsed': timeout
        }
    except Exception as e:
        return {
            'success': False,
            'returncode': -1,
            'stdout': '',
            'stderr': f'Error: {type(e).__name__}: {e}',
            'elapsed': 0
        }


@mcp.tool()
def run_python_code(code: str) -> str:
    """
    Execute Python code and return the result.
    """
    if not code.strip():
        return "Error: Code cannot be empty"
    
    result = execute_python_code(code, timeout=10)
    
    output = []
    output.append(f"=== Execution Result ===")
    output.append(f"Execution time: {result['elapsed']:.3f}s")
    output.append(f"Return code: {result['returncode']}")
    
    if result['success']:
        output.append("Status: ✓ Success")
        if result['stdout']:
            output.append(f"\nStandard Output:\n{result['stdout']}")
        if result['stderr']:
            output.append(f"\nStandard Error:\n{result['stderr']}")
    else:
        output.append("Status: ✗ Failed")
        if result['stderr']:
            output.append(f"\nError Message:\n{result['stderr']}")
        if result['stdout']:
            output.append(f"\nOutput Message:\n{result['stdout']}")
    
    return "\n".join(output)



if __name__ == "__main__":
    mcp.run()