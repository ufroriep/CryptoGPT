
import feedparser
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

def fetch_news_sentiment(coin='bitcoin'):
    # Beispielhafte Newsfeeds (CoinDesk)
    url = f'https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml'
    feed = feedparser.parse(url)
    analyzer = SentimentIntensityAnalyzer()

    sentiment_data = []
    for entry in feed.entries[:20]:
        published = datetime(*entry.published_parsed[:6])
        text = entry.title + " " + entry.summary
        score = analyzer.polarity_scores(text)['compound']
        sentiment_data.append({'date': published.date(), 'score': score})

    df_sentiment = pd.DataFrame(sentiment_data)
    daily_sentiment = df_sentiment.groupby('date').mean()
    daily_sentiment.index = pd.to_datetime(daily_sentiment.index)
    return daily_sentiment
