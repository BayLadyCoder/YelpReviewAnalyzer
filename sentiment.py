from textblob import TextBlob

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
            popularScores -= 1

        count += 1
        sentimentScores += score

        # print('*******************************************')
        # print(review, 'score', score)
        # print('*******************************************')

    finalPopularScore = round((popularScores/count)*100, 2)
    finalSentimentScore = round(((sentimentScores/count))*100, 2)
    analyzedData['sentiment'] = finalSentimentScore
    analyzedData['popular'] = finalPopularScore
    # print('sentiment score:', finalSentimentScore, '%')
    # print('test score:', finalPopularScore, '%')

    if finalSentimentScore > 30:
        analyzedData['summary'] = 'This restaurant got the best compliments'
        analyzedData['img'] = 'best.png'
    elif finalSentimentScore > 25:
        analyzedData['summary'] = 'This restaurant is excellent'
        analyzedData['img'] = 'exellent.png'
    elif finalSentimentScore > 20:
        analyzedData['summary'] = 'This restaurant is very good'
        analyzedData['img'] = 'verygood.png'
    elif finalSentimentScore > 15:
        analyzedData['summary'] = 'This restaurant is good'
        analyzedData['img'] = 'good.png'
    elif finalSentimentScore > 10:
        analyzedData['summary'] = 'This restaurant is average'
        analyzedData['img'] = 'ok.png'
    elif finalSentimentScore > 5:
        analyzedData['summary'] = 'This restaurant is okay'
        analyzedData['img'] = 'okay.png'

    elif finalSentimentScore > 0:
        analyzedData['summary'] = 'This restaurant is not so good'
        analyzedData['img'] = 'bad.png'
    else:
        analyzedData['summary'] = "Stay away from this restaurant!"
        analyzedData['img'] = 'worse.png'

    return analyzedData


# https://github.com/ssut/py-googletrans
# https://cloud.google.com/translate/docs
# todo: replace textblob with google translate
def translate(reviews, language):
    translatedReviews = []

    for review in reviews:
        blob = TextBlob(review)
        if language == 'th':
            review = blob.translate(from_lang='en',to='th')
        elif language == 'es':
            review = blob.translate(from_lang='en',to='es')
        elif language == 'zh-CN':
            review = blob.translate(from_lang='en',to='zh-CN')
        else:
            review = review
        translatedReviews.append(review)

    return translatedReviews

