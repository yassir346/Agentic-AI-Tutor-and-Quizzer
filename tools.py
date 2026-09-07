import ast
import operator

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

CALCULATOR_TOOL_SCHEMA = {
    "name": "calculate",
    "description": "Evaluates a basic arithmetic expression and returns the numeric result. Use this any time exact math is needed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A math expression to evaluate, e.g. '12 * (7 + 3)'"
            }
        },
        "required": ["expression"]
    }
}

def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression element: {node}")


def calculate(expression):
    """Safely evaluate a basic arithmetic expression and return the result."""
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body)


SEARCH_NOTES_TOOL_SCHEMA = {
    "name": "search_notes",
    "description": "Searches the learner's study notes for entries matching a keyword or topic and returns the matching note(s). Use this whenever the learner asks about a specific AI agent concept, to ground your answer in their actual notes rather than general knowledge.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A keyword or short phrase to search for, e.g. 'tool use' or 'memory'"
            }
        },
        "required": ["query"]
    }
}

def load_notes(filepath="notes.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pieces = [p.strip() for p in content.split("\n\n") if p.strip()]
    # pieces alternate: title, body, title, body, ... because of how the file is formatted
    entries = []
    for i in range(0, len(pieces) - 1, 2):
        entries.append(f"{pieces[i]}\n{pieces[i + 1]}")
    return entries

def search_notes(query):
    entries = load_notes()
    query_lower = query.lower()
    matches = [entry for entry in entries if query_lower in entry.lower()]
    if not matches:
        return "No matching notes found."
    return "\n\n---\n\n".join(matches)

ASK_QUIZZER_TOOL_SCHEMA = {
    "name": "ask_quizzer",
    "description": "Delegates to a specialized quiz-writing agent that generates one quiz question (with its answer) on a given topic. Use this when the learner wants to test their knowledge.",
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "The topic to quiz on, e.g. 'tool use'"}
        },
        "required": ["topic"]
    }
}
