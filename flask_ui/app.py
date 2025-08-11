from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# URL for your Rasa server's REST endpoint
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"User message received: {user_message}")

    # Prepare payload for Rasa
    payload = {
        "sender": "user", # You can use a unique ID for each user if needed
        "message": user_message
    }

    try:
        # Send message to Rasa
        rasa_response = requests.post(RASA_API_URL, json=payload)
        rasa_response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse Rasa's response
        bot_responses = rasa_response.json()
        print(f"Rasa raw response: {json.dumps(bot_responses, indent=2)}")

        # Extract text responses from Rasa
        messages_to_send = []
        for response in bot_responses:
            if "text" in response:
                messages_to_send.append({"sender": "bot", "text": response["text"]})
            # Handle other response types like images, buttons if Rasa sends them
            # if "image" in response:
            #     messages_to_send.append({"sender": "bot", "image": response["image"]})

        if not messages_to_send:
            messages_to_send.append({"sender": "bot", "text": "I didn't get a clear response from my AI brain. Can you rephrase?"})

        return jsonify(messages_to_send)

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not connect to Rasa server. Is it running?"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with Rasa: {e}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode JSON from Rasa response."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000) # Run Flask app on port 5000