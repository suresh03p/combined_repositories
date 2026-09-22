import ast
import operator

from app.tools.errors import ToolError

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval")
        value = _evaluate(tree.body)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ToolError("Unsupported calculation") from error
    return str(value)


def _evaluate(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    raise ValueError("Invalid expression")
