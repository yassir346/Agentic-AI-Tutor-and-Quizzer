import anthropic
from tools import calculate, search_notes

client = anthropic.Anthropic(api_key="fake-key-for-now")

def run_agent(user_message, tools_schema, system="", max_rounds=5, model="claude-sonnet-5"):
    messages = [{"role": "user", "content": user_message}]
    for _ in range(max_rounds):
        response = client.messages.create(
            model=model,
            max_tokens=300,
            tools=tools_schema,
            system=system,
            messages=messages,
        )
        if response.stop_reason != "tool_use":
            text_block = next(b for b in response.content if b.type == "text")
            return text_block.text
        messages.append({"role": "assistant", "content": response.content})
        tool_result_blocks = []
        for block in response.content:
            if block.type == "tool_use":
                fn = TOOL_FUNCTIONS[block.name]
                try:
                    result = fn(**block.input)
                    content_str = str(result)
                    print(f"[tool call] {block.name}({block.input}) -> {content_str[:150]}")
                except Exception as e:
                    content_str = f"Error: {e}"
                tool_result_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content_str,
                })
        messages.append({"role": "user", "content": tool_result_blocks})
    raise RuntimeError("Agent didn't finish within max_rounds")

from quizzer_agent import ask_quizzer

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "search_notes": search_notes,
    "ask_quizzer": ask_quizzer,
}