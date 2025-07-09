from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from typing import Optional

app = FastAPI()


def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


class ReviewInput(BaseModel):
    text: str


class ReviewOutput(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


def analyze_sentiment(text: str) -> str:
    text = text.lower()
    positive_words = ['хорош', 'люблю', 'нравится', 'отличн', 'прекрасн', 'супер', 'класс']
    negative_words = ['плохо', 'ненавиж', 'ужасн', 'отвратительн', 'кошмар', 'разочарован']

    if any(word in text for word in positive_words):
        return 'positive'
    elif any(word in text for word in negative_words):
        return 'negative'
    return 'neutral'


@app.post("/reviews", response_model=ReviewOutput)
async def create_review(review: ReviewInput):
    sentiment = analyze_sentiment(review.text)
    created_at = datetime.now().isoformat()

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
        (review.text, sentiment, created_at)
    )
    review_id = cursor.lastrowid
    conn.commit()

    cursor.execute(
        "SELECT id, text, sentiment, created_at FROM reviews WHERE id = ?",
        (review_id,)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=500, detail="Failed to create review")

    return {
        "id": result[0],
        "text": result[1],
        "sentiment": result[2],
        "created_at": result[3]
    }


@app.get("/reviews", response_model=list[ReviewOutput])
async def get_reviews(sentiment: Optional[str] = None):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    if sentiment:
        cursor.execute(
            "SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?",
            (sentiment,)
        )
    else:
        cursor.execute(
            "SELECT id, text, sentiment, created_at FROM reviews"
        )

    results = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "text": row[1],
            "sentiment": row[2],
            "created_at": row[3]
        }
        for row in results
    ]