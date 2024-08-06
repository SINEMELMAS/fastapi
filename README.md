# fastapi
from fastapi import FastAPI
from langdetect import detect
import spacy
from collections import Counter
from textblob import TextBlob
from transformers import pipeline
import nltk
nltk.download('words')
from nltk.corpus import words

app = FastAPI()

# Load resources
english_words = set(words.words())
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = spacy.load('en_core_web_sm')


@app.post('/summary', summary="Summary of your text", tags=["sum"])
async def summarization_(text):
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

        words = [token.text for token in doc if not token.is_stop and not token.is_punct]
        freq_word = Counter(words)
        keywords = [word for word, freq in freq_word.most_common(5)]

        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

        sum_dic = {
            "Sentiment": sentiment,
            "Keywords": keywords,
            "Summary": summary[0]['summary_text']
        }

        return sum_dic
    else:
        return "Sorry, this program only supports the English language!"

    #text = ("The sun set over the small town of Everwood, casting long shadows across the cobblestone streets.In the heart of the town, the old clock tower chimed seven times, its echoes fading into the cool evening air. A gentle breeze rustled the leaves of the ancient oak tree in the town square, where children played and laughter filled the air. Shopkeepers began closing their stores, waving goodnight to each other as they headed home. The aroma of freshly baked bread wafted from the bakery, mingling with the scent of blooming flowers from Mrs. Whitaker’s garden. As the stars appeared one by one in the twilight sky, the townsfolk settled into their homes, ready to rest and dream of another peaceful day in Everwood.")

