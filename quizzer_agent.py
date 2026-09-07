from agent_loop import run_agent

QUIZZER_SYSTEM_PROMPT = """You are a quiz master for an AI agent concepts course.
Given a topic, write one short quiz question about it, then on the next line
give the correct answer, prefixed with "Answer:". Keep it concise."""

def ask_quizzer(topic):
    return run_agent(
        user_message=f"Create a quiz question about: {topic}",
        tools_schema=[],
        system=QUIZZER_SYSTEM_PROMPT,
        model="claude-haiku-4-5"
    )

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


