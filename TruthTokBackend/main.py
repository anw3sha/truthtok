import flask
from flask import Flask, request
from flask_cors import CORS
from scrape_verify import construct_search_url, scrape, verify
from databaseConnection import dbConnection
app = Flask(__name__)
import pyktok
import openai
from openai import OpenAI
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
# Talisman(app)
CORS(app, headers=["Content-Type", "Authorization"])

@app.route("/analyzeLink")
def analyze():
    #recieves link and does speech to text & image to text and returns total text
    link = request.data

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


@app.route("/getAccount")
def getAccount():
    accID = request.args.get("accountID")
    return db.getAccount(accID)

@app.route("/newTikTok")
def newTiktok():

# example usage
# keywords = "diddy party on 10/15"
# articles = scrape(keywords)
# classification = classify(articles)
# print(classification)
# returns check, question, cross

if __name__ == "__main__":
    db = dbConnection()

    app.run(port=3004)