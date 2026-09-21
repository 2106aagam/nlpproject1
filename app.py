from flask import Flask, render_template, request, jsonify
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)
DB = "data/sentiment.db"

POSITIVE_WORDS = {
    "amazing": 3, "awesome": 3, "excellent": 3, "fantastic": 3, "great": 2,
    "good": 2, "happy": 2, "love": 3, "loved": 3, "like": 2, "liked": 2,
    "wonderful": 3, "best": 3, "beautiful": 2, "enjoy": 2, "enjoyed": 2,
    "perfect": 3, "nice": 2, "success": 2, "successful": 2, "helpful": 2,
    "fun": 2, "brilliant": 3, "super": 2, "positive": 2, "recommend": 2,
    "satisfied": 2, "thank": 1, "thanks": 1, "easy": 1, "excited": 2
}

NEGATIVE_WORDS = {
    "bad": 2, "terrible": 3, "horrible": 3, "awful": 3, "worst": 3,
    "hate": 3, "hated": 3, "dislike": 2, "disliked": 2, "sad": 2,
    "angry": 2, "poor": 2, "boring": 2, "boring": 2, "disappointing": 3,
    "disappointed": 3, "problem": 1, "problems": 1, "fail": 2, "failed": 2,
    "failure": 2, "slow": 1, "difficult": 1, "useless": 3, "negative": 2,
    "error": 2, "errors": 2, "broken": 2, "late": 1, "expensive": 1
}

NEGATIONS = {"not", "never", "no", "don't", "didn't", "isn't", "wasn't", "can't", "cannot"}

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def tokenize(text):
    return re.findall(r"[A-Za-z']+", text.lower())

def analyze_sentiment(text):
    tokens = tokenize(text)
    if not tokens:
        return "Neutral", 0.50, 0

    score = 0
    positive_hits = []
    negative_hits = []

    for i, word in enumerate(tokens):
        value = 0
        if word in POSITIVE_WORDS:
            value = POSITIVE_WORDS[word]
            positive_hits.append(word)
        elif word in NEGATIVE_WORDS:
            value = -NEGATIVE_WORDS[word]
            negative_hits.append(word)

        # Simple NLP negation handling: "not good" -> negative
        if value != 0 and i > 0 and tokens[i - 1] in NEGATIONS:
            value *= -1
            if value > 0:
                positive_hits.append(word)
            else:
                negative_hits.append(word)
        score += value

    # Light intensifier handling
    for i, word in enumerate(tokens):
        if word in {"very", "really", "extremely", "so"} and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if nxt in POSITIVE_WORDS:
                score += 0.5
            elif nxt in NEGATIVE_WORDS:
                score -= 0.5

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Confidence is a simple normalized indicator, not a statistical probability.
    confidence = min(0.99, 0.50 + min(abs(score), 8) * 0.06)
    return sentiment, confidence, score

def save_history(text, sentiment, confidence):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO history(text, sentiment, score, created_at) VALUES (?, ?, ?, ?)",
        (text, sentiment, confidence, datetime.now().strftime("%d %b %Y, %I:%M %p"))
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or request.form
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    sentiment, confidence, raw_score = analyze_sentiment(text)
    save_history(text, sentiment, confidence)

    return jsonify({
        "sentiment": sentiment,
        "confidence": round(confidence * 100, 1),
        "score": raw_score,
        "word_count": len(tokenize(text))
    })

@app.route("/history")
def history():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT text, sentiment, score, created_at FROM history ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return render_template("history.html", rows=rows)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/clear-history", methods=["POST"])
def clear_history():
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
