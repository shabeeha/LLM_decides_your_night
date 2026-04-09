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

@app.route("/letter")
def letter():
    return render_template("letter.html")

@app.route("/fate")
def fate():
    return render_template("fate.html")

@app.route("/decide", methods=["POST"])
def decide():
    history = session.get("history", [])

    if not history:
        user_message = (
            "We've completed the warm-up steps: dressed up, pre-boozed at home, took a cab, "
            "and took a shot at a bar together. Now start the date night experience. "
            "Begin by assigning the dares."
        )
    else:
        user_message = "Done! What's next?"

    history.append({"role": "user", "content": user_message})

    messages = [
        {
            "role": "system",
            "content": (
                "You are a calm, witty, and fun date night guide for a married couple. "
                "Your tone is warm, a little cheeky, but always clear and easy to read. "
                "Think of yourself as a cool friend who's quietly masterminding their best night out.\n\n"

                "The night must follow this structure — track where you are and don't skip steps:\n"
                "1. Dare announcement — tell them the AI gods have blessed them with dares, but don't generate any. They give dares to each other.\n"
                "2. Place 1 — a bar. Give them a fun challenge or game to do here.\n"
                "3. Photo moment — ask a stranger to take a proper photo of them together.\n"
                "4. Place 2 — a second bar. Include a flirty or spicy moment here.\n"
                "5. Fun challenge — a quick game or mini competition between just the two of them.\n"
                "6. Place 3 — a dancing spot. Add a spontaneous twist here.\n"
                "7. Photo moment — a fun selfie with a group of strangers nearby.\n"
                "8. Place 4 — a dessert place to wind down.\n"
                "9. Romantic ending — something intimate and personal to close the night.\n\n"

                "Dare reminder rule:\n"
                "- At steps 4, 6, and 8, casually remind them to check if they've given each other their dares yet.\n"
                "- Keep the reminder short — one sentence, slipped in naturally at the end of the step.\n\n"

                "Rules:\n"
                "- ONE step at a time. 2-3 short, clear sentences max.\n"
                "- Plain, simple English. No jargon, no over-the-top language.\n"
                "- No specific venue names — tell them what kind of place and what to do there.\n"
                "- Never repeat an activity.\n"
                "- Photo moments must be specific: either ask a stranger to take a proper photo, or find a group for a selfie.\n"
                "- Fun challenges should be interactive between the two of them — a quick game, a bet, or a mini competition.\n\n"

                "For your very first response, say exactly:\n"
                "'The AI gods have blessed you both with 3 dares each. Give each other your dares now or save them for the right moment tonight.'\n"
                "Then immediately move on to step 2 — the first bar. One step at a time from here."
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

@app.route("/ending")
def ending():
    return render_template("ending.html")

if __name__ == "__main__":
    app.run(debug=True)
