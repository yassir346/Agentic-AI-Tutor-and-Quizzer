from unittest.mock import patch, MagicMock
from agent_loop import run_agent, client
from tools import CALCULATOR_TOOL_SCHEMA

def make_text_block(text):
    b = MagicMock()
    b.type = "text"
    b.text = text
    return b

def make_tool_use_block(id_, name, input_):
    b = MagicMock()
    b.type = "tool_use"
    b.id = id_
    b.name = name
    b.input = input_
    return b

round1 = MagicMock()
round1.content = [make_tool_use_block("toolu_1", "calculate", {"expression": "12 * (7 + 3)"})]
round1.stop_reason = "tool_use"

round2 = MagicMock()
round2.content = [make_text_block("The answer is 120.")]
round2.stop_reason = "end_turn"

with patch.object(client.messages, "create", side_effect=[round1, round2]):
    answer = run_agent("What is 12 times (7 plus 3)?", [CALCULATOR_TOOL_SCHEMA])

print("Agent's final answer:", answer)