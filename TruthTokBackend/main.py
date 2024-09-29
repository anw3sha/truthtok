import flask
from flask import Flask, request
from flask_cors import CORS
from scrape_verify import construct_search_url, scrape, classify
from get_text import download_vid, get_audio, detect_text, process_video
from databaseConnection import dbConnection
import json
app = Flask(__name__)
import openai
from openai import OpenAI

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
# Talisman(app)
CORS(app)
def detectKeyWords(text):
    # take in all tiktok text and detect keywords
    client = OpenAI()
    totalText = "Summarize this text in 10 words: " + text
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": totalText}
        ]
    )
    return completion["choices"]["message"]["content"]
@app.route("/analyzeLink", methods=["POST"])

def analyze():
    # recieves link and does speech to text & image to text and returns total text
    print("HI")
    link = json.loads(request.data)["link"]
    print("2")
    video = download_vid(link)
    print("3")
    transcription_file = get_audio(video)
    print("4")
    username, detected_text = process_video(video)
    print("5")
    print("6")
    full_text = transcription_file + detected_text
    print("7")
    keywords = detectKeyWords(full_text)
    print("8")
    articles = scrape(keywords)
    print("9")
    classification = classify(articles)
    print("10")
    if classification == "check":
        return "check"
    elif classification == "cross":
        return "cross"
    else: return "question"

    # returns check, question, cross

@app.route("/getAccount")
def getAccount():
    accID = request.args.get("accountID")
    return db.getAccount(accID)



if __name__ == "__main__":
    db = dbConnection()
    app.run(port=3004)