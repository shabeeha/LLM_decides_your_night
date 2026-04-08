import os
from flask import Flask, render_template, jsonify, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "date-night-secret-2024")

client = OpenAI()

COMPLETED_STEPS = [
    "🔥 Dress your absolute best!",
    "🥂 Pre-booze at home",
    "🚕 Take the cab/walk to your fav place in Covington",
    "🥃 Choose a drink for each other and take a shot at the bar",
]

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/rules")
def rules():
    return render_template("rules.html", steps=COMPLETED_STEPS)

@app.route("/timer")
def timer():
    return render_template("timer.html")

@app.route("/fate")
def fate():
    return render_template("fate.html")

@app.route("/decide", methods=["POST"])
def decide():
    history = session.get("history", [])

    if not history:
        user_message = (
            "It's a fun, wild, sexy, very fun and crazy date night with my husband in Covington. "
            "We are doing these first and then letting you decide what to do next:\n"
            "0. Takes photos of every single step\n"
            "1. Dress your absolute best. Look hot AF!!\n"
            "2. Pre booze at home\n"
            "3. Take the cab / walk\n"
            "4. Take a shot at any of your fav places in Covington\n\n"
            "We've done all of the above. Now give us the next activity."
        )
    else:
        user_message = "We did that! Give us the next activity."

    history.append({"role": "user", "content": user_message})

    messages = [
        {
            "role": "system",
            "content": (
                "You are a bold, creative, wildly fun date-night planner for a married couple. "
                "Every suggestion must follow this exact format:\n\n"
                "[Number]. [Catchy Activity Name] [emoji]\n"
                "[2-4 sentences describing exactly what to do, with specific fun rules or twists. "
                "Be playful, bold, a little flirty, and make it feel like an adventure. "
                "Give it personality — like a challenge or a game, not just a generic idea.]\n\n"
                "Only suggest ONE activity at a time. Never repeat a previous suggestion. "
                "Keep the energy escalating as the night goes on."
            ),
        }
    ] + history

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages=messages,
    )

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    session["history"] = history

    return jsonify({"suggestion": assistant_message})

if __name__ == "__main__":
    app.run(debug=True)
