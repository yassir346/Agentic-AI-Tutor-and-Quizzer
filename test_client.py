from unittest.mock import patch, MagicMock
import anthropic

client = anthropic.Anthropic(api_key="fake-key-for-now")

fake_text_block = MagicMock()
fake_text_block.type = "text"
fake_text_block.text = "Hello! I'm a mocked Claude response."

fake_response = MagicMock()
fake_response.id = "msg_fake123"
fake_response.type = "message"
fake_response.role = "assistant"
fake_response.content = [fake_text_block]
fake_response.model = "claude-haiku-4-5"
fake_response.stop_reason = "end_turn"
fake_response.usage.input_tokens = 10
fake_response.usage.output_tokens = 8

with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()
    print(len(system_prompt))

with patch.object(client.messages, "create", return_value=fake_response):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        system=system_prompt,
        messages=[{"role": "user", "content": "Hello, Claude!"}]
    )
    print("Reply text:", response.content[0].text)
    print("Stop reason:", response.stop_reason)
    print("Tokens - input:", response.usage.input_tokens, "output:", response.usage.output_tokens)


# try:
#     response = client.messages.create(
#         model="claude-haiku-4-5",
#         max_tokens=100,
#         messages=[
#             {"role": "user", "content": "Hello, Claude!"}
#         ]
#     )
#     print(response)
# except anthropic.AnthropicError as e:
#     print("Got an authentication error, as expected:")
#     print(e)