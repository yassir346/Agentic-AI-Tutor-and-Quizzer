from unittest.mock import patch, MagicMock
import anthropic
from tools import calculate, CALCULATOR_TOOL_SCHEMA

client = anthropic.Anthropic(api_key="fake-key-for-now")

fake_tool_block = MagicMock()
fake_tool_block.type = "tool_use"
fake_tool_block.id = "toolu_fake001"
fake_tool_block.name = "calculate"
fake_tool_block.input = {"expression": "12 * (7 + 3)"}

fake_response = MagicMock()
fake_response.content = [fake_tool_block]
fake_response.stop_reason = "tool_use"

with patch.object(client.messages, "create", return_value=fake_response):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        tools=[CALCULATOR_TOOL_SCHEMA],
        messages=[{"role": "user", "content": "What is 12 times (7 plus 3)?"}]
    )

if response.stop_reason == "tool_use":
    tool_call = next(block for block in response.content if block.type == "tool_use")
    print("Claude wants to call:", tool_call.name, "with input:", tool_call.input)
        
    result = calculate(**tool_call.input)
    print("Real function result:", result)

    tool_result_message = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": str(result)
            }
        ]
    }
    print("Message to send back to Claude:", tool_result_message)
    
