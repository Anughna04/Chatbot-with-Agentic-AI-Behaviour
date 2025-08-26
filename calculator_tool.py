#Calculator Tool - Simple math operations

import re
from typing import Dict, Any

class CalculatorTool:
    def calculate(self, expression: str) -> Dict[str, Any]:
        expr = expression.lower().strip()
        try:
            numbers = [float(x) for x in re.findall(r"-?\d+\.?\d*", expr)]
            if len(numbers) != 2:
                return {"success": False, "error": "Could not parse numbers"}

            a, b = numbers
            if any(op in expr for op in ["add", "+", "plus"]):
                return {"success": True, "result": a + b, "operation": "addition"}
            elif any(op in expr for op in ["subtract", "-", "minus"]):
                return {"success": True, "result": a - b, "operation": "subtraction"}
            elif any(op in expr for op in ["multiply", "*", "x", "times"]):
                return {"success": True, "result": a * b, "operation": "multiplication"}
            elif any(op in expr for op in ["divide", "/", "÷"]):
                if b == 0:
                    return {"success": False, "error": "Division by zero"}
                return {"success": True, "result": a / b, "operation": "division"}
            else:
                return {"success": False, "error": "Unknown operation"}
        except Exception as e:
            return {"success": False, "error": str(e)}
