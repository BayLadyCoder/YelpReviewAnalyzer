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


count = 0
posScores = 0
negScores = 0
with open('theReviews.txt', 'r') as f:
    for line in f.read().split('\n'):
        reviewBlob = TextBlob(line)
        # print('Translate to Thai:', reviewBlob.translate(to='th'))
        score = reviewBlob.sentiment.polarity
        if score > 0.5:
            posScores += 1
        elif score > 0:
            posScores += 0.5
        elif score > 0.5:
            negScores -= 0.5
        else:
            negScores -= 1
        count+=1
    finalScore = ((posScores+negScores/count)/count)*100
    print(finalScore, '%')

    if finalScore > 90:
        print('This restaurant is exellent')
    elif finalScore > 80:
        print('This restaurant is very good')
    elif finalScore > 70:
        print('This restaurant is decent')
    elif finalScore > 60:
        print('This restaurant is good')
    elif finalScore > 50:
        print('This restaurant is so So')
    elif finalScore > 40:
        print('This restaurant is not so good')
    elif finalScore > 30:
        print('This restaurant is bad')
    elif finalScore > 20:
        print('This restaurant is very bad')
    else:
        print("Don't go to this restaurant")


