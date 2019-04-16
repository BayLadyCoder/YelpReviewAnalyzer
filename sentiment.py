from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

blob = TextBlob("My cats are very heavy")

# See all methods
# print(dir(blob))

print(blob.tags)


# polarity (from -1 to 1 negative to positive)
# subjectivity (from 0 to 1, 0 is objective and 1 is subjective)
print(blob.sentiment)
print('Polarity:', blob.sentiment.polarity)
print('Subjectivity:', blob.sentiment.subjectivity)

print('Translate to Thai:', blob.translate(to='th'))
print('Translate to Spanish:', blob.translate(to='es'))
print('Translate to Arabic:', blob.translate(to='ar'))
print('Translate to Chinese:', blob.translate(to='zh-CN'))