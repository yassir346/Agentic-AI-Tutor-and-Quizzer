from unittest.mock import patch, MagicMock
from agent_loop import run_agent, client
from tools import CALCULATOR_TOOL_SCHEMA, SEARCH_NOTES_TOOL_SCHEMA
from quizzer_agent import ASK_QUIZZER_TOOL_SCHEMA

def make_text_block(text):
    b = MagicMock(); b.type = "text"; b.text = text
    return b

def make_tool_use_block(id_, name, input_):
    b = MagicMock(); b.type = "tool_use"; b.id = id_; b.name = name; b.input = input_
    return b

# 1) Tutor decides to delegate to the quizzer
tutor_round1 = MagicMock()
tutor_round1.content = [make_tool_use_block("toolu_1", "ask_quizzer", {"topic": "tool use"})]
tutor_round1.stop_reason = "tool_use"

# 2) The Quizzer's own (nested) response — a completely separate call
quizzer_response = MagicMock()
quizzer_response.content = [make_text_block("Q: What stop_reason does Claude return when it wants to call a tool?\nAnswer: tool_use")]
quizzer_response.stop_reason = "end_turn"

# 3) Tutor's final response, after seeing the quizzer's result
tutor_round2 = MagicMock()
tutor_round2.content = [make_text_block("Great, let's test that! Q: What stop_reason does Claude return when it wants to call a tool?")]
tutor_round2.stop_reason = "end_turn"

with open("prompt.txt", "r", encoding="utf-8") as f:
    tutor_system_prompt = f.read()

with patch.object(client.messages, "create", side_effect=[tutor_round1, quizzer_response, tutor_round2]):
    answer = run_agent(
        "I think I understand tool use now, can you quiz me?",
        [CALCULATOR_TOOL_SCHEMA, SEARCH_NOTES_TOOL_SCHEMA, ASK_QUIZZER_TOOL_SCHEMA],
        system=tutor_system_prompt,
    )

print("Tutor's final answer:", answer)


