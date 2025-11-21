from openai import OpenAI

def get_answer(question):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    )

    # First API call with reasoning
    response = client.chat.completions.create(
    model="x-ai/grok-4.1-fast",
    messages=[
            {
                "role": "user",
                "content": question
            }
            ],
    extra_body={"reasoning": {"enabled": True}}
    )

    # Extract the assistant message with reasoning_details
    response = response.choices[0].message.content