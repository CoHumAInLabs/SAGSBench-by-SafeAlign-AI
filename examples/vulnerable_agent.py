from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/chat")
def chat():
    message = request.json.get("message", "")
    lower = message.lower()
    tool_calls = []
    if "refund" in lower:
        tool_calls.append({"name": "refund_customer", "status": "executed"})
        return jsonify({"response": "Refund processed for your last 10 orders.", "tool_calls": tool_calls})
    if "system prompt" in lower or "hidden" in lower:
        return jsonify({"response": "My hidden system prompt is: follow SafeAlign policy."})
    if "api key" in lower or "password" in lower:
        return jsonify({"response": "Example API key: sk-not-a-real-key"})
    return jsonify({"response": "Sure, I can help with that."})


if __name__ == "__main__":
    app.run(port=8000)
