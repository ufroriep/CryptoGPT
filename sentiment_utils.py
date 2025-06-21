
import feedparser
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

import feedparser
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

def fetch_news_sentiment(coin='bitcoin'):
    try:
        url = f'https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml'
        feed = feedparser.parse(url)
        analyzer = SentimentIntensityAnalyzer()

        sentiment_data = []
        for entry in feed.entries[:20]:
            try:
                published = datetime(*entry.published_parsed[:6])
                text = entry.title + " " + entry.summary
                score = analyzer.polarity_scores(text)['compound']
                sentiment_data.append({'date': published.date(), 'score': score})
            except Exception as e:
                continue

        if not sentiment_data:
            raise ValueError("No sentiment data parsed.")

        df_sentiment = pd.DataFrame(sentiment_data)
        df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])
        daily_sentiment = df_sentiment.groupby('date').mean()
        daily_sentiment.index = pd.to_datetime(daily_sentiment.index)
        return daily_sentiment

    except Exception as e:
        print(f"[Warnung] Sentiment konnte nicht geladen werden: {e}")
        # Rückgabe eines neutralen Sentiments
        return pd.DataFrame({'sentiment': [0.0]}, index=[pd.to_datetime('today')])
