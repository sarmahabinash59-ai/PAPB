
from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import urllib.error
import json
import base64
import os

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "gemma3:4b"


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


@app.route("/api/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "").strip()
    image = request.files.get("image")

    if not message and not image:
        return jsonify({"reply": "Please type a question or upload a plant photo."}), 400

    user_message = (
        "You are Plant Bot, an agricultural assistant. Help identify plant "
        "diseases and pests from symptoms or photos. Give likely causes, "
        "visible evidence, practical management, and prevention. Be cautious: "
        "if uncertain, say so. Do not claim a definite diagnosis from an unclear photo. "
        "Recommend checking local agricultural extension guidance before pesticide use.\n\n"
        + (message or "Examine this plant photo and describe any visible symptoms.")
    )

    user_content = {"role": "user", "content": user_message}

    if image:
        image_bytes = image.read()
        user_content["images"] = [base64.b64encode(image_bytes).decode("utf-8")]

    payload = {
        "model": MODEL,
        "messages": [user_content],
        "stream": False,
        "options": {"num_predict": 80}
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        reply = result.get("message", {}).get("content", "Sorry, I could not generate a response.")
        return jsonify({"reply": reply})

    except urllib.error.URLError:
        return jsonify({
            "reply": "I cannot reach Ollama. Please make sure Ollama is running on your computer."
        }), 503
    except Exception as error:
        return jsonify({"reply": "An error occurred: " + str(error)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
