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



def analyzeReviews(reviewList):
    count = 0
    sentimentScores = 0
    analyzedData = {}
    popularScores = 0
    for review in reviewList:
        reviewBlob = TextBlob(review)
        score = reviewBlob.sentiment.polarity
        
    
        if score > 0:
            popularScores += 1
        elif score < 0:
            popularScores -=1
        
        count+=1
        sentimentScores+=score

        print('*******************************************')
        # print(review,'score', score, 'positive: ', posScores, 'negative', negScores)
        print(review,'score', score)
        print('*******************************************')
        
    finalPopularScore = (popularScores/count)*100
    finalSentimentScore = ((sentimentScores/count))*100
    analyzedData['sentiment'] = finalSentimentScore
    analyzedData['popular'] = finalPopularScore
    print('sentiment score:', finalSentimentScore, '%')
    print('test score:', finalPopularScore, '%')


    if finalSentimentScore > 30:
        analyzedData['summary'] = 'This restaurant is exellent'
    elif finalSentimentScore > 25:
        analyzedData['summary'] = 'This restaurant is very good'
    elif finalSentimentScore > 20:
        analyzedData['summary'] = 'This restaurant is decent'
    elif finalSentimentScore > 15:
        analyzedData['summary'] = 'This restaurant is good'
    elif finalSentimentScore > 10:
        analyzedData['summary'] = 'This restaurant is okay'
    elif finalSentimentScore > 5:
        analyzedData['summary'] = 'This restaurant is so so'
    elif finalSentimentScore > 0:
        analyzedData['summary'] = 'This restaurant is not so good'
    else:
        analyzedData['summary'] = "Don't go to this restaurant"

    return analyzedData
