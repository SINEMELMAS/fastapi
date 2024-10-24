from fastapi import FastAPI, Body, HTTPException
from langdetect import detect
import spacy
from collections import Counter
from textblob import TextBlob
from transformers import pipeline
import nltk
from pymongo import MongoClient
from pymongo.server_api import ServerApi

nltk.download('words')
from nltk.corpus import words

app = FastAPI()

uri = "mongodb+srv://sinem34elmas:*****@cluster0.m03cb.mongodb.net/mydatabase?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi(version='1'))
db = client["mydatabase"]
collection = db["mycollection"]

db.mycollection.find();


english_words = set(words.words())
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = spacy.load('en_core_web_sm')

@app.post('/summary', summary="Summary of your text", tags=["sum"])
async def summarization_(text: str = Body(..., embed=True)):
    try:
        check_language = detect(text)
        if check_language == "en":
            doc = nlp(text)
            blob = TextBlob(text)

            if blob.sentiment.polarity > 0:
                sentiment = "Positive"
            elif blob.sentiment.polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            words_list = [token.text for token in doc if not token.is_stop and not token.is_punct]
            freq_word = Counter(words_list)
            keywords = [word for word, freq in freq_word.most_common(5)]

            summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

            sum_dic = {
                "Sentiment": sentiment,
                "Keywords": keywords,
                "Summary": summary[0]['summary_text']
            }

            result = collection.insert_one({
                "text": text,
                "summary": summary[0]['summary_text']
            })

            return {
                "inserted_id": str(result.inserted_id),
                "summary_data": sum_dic
            }
        else:
            raise HTTPException(status_code=400, detail="Sorry, this program only supports the English language!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

