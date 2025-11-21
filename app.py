from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re

app = Flask(__name__)

# Initialize OpenRouter client (Grok)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# ----------------------------
#  CLEAN + FORMAT ANSWER
# ----------------------------
def strip_markdown(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove bold/markdown symbols
    cleaned = (
        text.replace("**", "")
            .replace("__", "")
            .replace("`", "")
            .replace("*", "")
    )

    # Remove multiple whitespaces and line breaks
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


# ----------------------------
#   CALL GROK (OpenRouter)
# ----------------------------
def get_answer(question):
    response = client.chat.completions.create(
        model="x-ai/grok-4.1-fast",
        messages=[{"role": "user", "content": question}],
        extra_body={"reasoning": {"enabled": True}}
    )

    answer = response.choices[0].message.content
    return strip_markdown(answer)


# ----------------------------
#   ROUTES
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    # Basic preprocessing
    processed = question.lower().strip()

    # Call Grok LLM
    try:
        answer = get_answer(question)
    except Exception as e:
        print("Error:", e)
        return jsonify({
            "processed": processed,
            "answer": "Error occurred while contacting the LLM."
        }), 500

    return jsonify({
        "processed": processed,
        "answer": answer
    })


if __name__ == '__main__':
    app.run(debug=True)
