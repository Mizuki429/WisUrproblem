from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
CORS(app, origins=["https://Mizuki429.github.io"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # 環境変数にAPIキーを設定しておくこと
MODEL = "anthropic/claude-3-opus"

@app.route("/ask", methods=["POST"])
def ask_claude():
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
    port = int(os.environ.get("PORT", 5000))  # PORT環境変数がなければ5000
    app.run(host="0.0.0.0", port=port)

