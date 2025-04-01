from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # CORSを全ルートで許可

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-3-opus"

@app.route("/", methods=["GET", "OPTIONS"])
def root():
    return "API is live", 200

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask_claude():
    if request.method == "OPTIONS":
        return '', 204  # CORSプリフライトへの返答

    data = request.get_json()
    trouble = data.get("trouble")
    reason = data.get("reason")

    if not trouble or not reason:
        return jsonify({"error": "Invalid input"}), 400

    prompt = f"""
困りごと: "{trouble}"
原因: "{reason}"
この人が働くときに必要な配慮事項を、できるだけ具体的に、3つ程度リストアップしてください。箇条書きで出力してください。
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return jsonify({"suggestion": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

