"""Calculator tool for MCP.

Provides safe mathematical expression evaluation.
"""

import ast
import operator
from typing import Any


# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_expr(node: ast.expr) -> float:
    """
    Safely evaluate an AST expression node.
    
    Args:
        node: AST expression node to evaluate.
        
    Returns:
        Evaluated result as a float.
        
    Raises:
        ValueError: If expression contains unsupported operations.
    """
    if isinstance(node, ast.Constant):
        return float(node.value)
    elif isinstance(node, ast.BinOp):
        left = _eval_expr(node.left)
        right = _eval_expr(node.right)
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_expr(node.operand)
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op(operand)
    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


def calculate(expression: str) -> dict[str, Any]:
    """
    Safely evaluate a mathematical expression.
    
    Supports basic arithmetic operations: +, -, *, /, ^ (power)
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5 - 3")
        
    Returns:
        Dictionary with expression and result.
        
    Raises:
        ValueError: If expression is invalid or contains unsupported operations.
    """
    try:
        # Parse expression into AST
        tree = ast.parse(expression, mode='eval')
        
        # Evaluate the expression
        result = _eval_expr(tree.body)
        
        return {
            "expression": expression,
            "result": result,
        }
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {str(e)}")
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Calculation error: {str(e)}")
