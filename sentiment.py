from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


def dictToJSOND3(dict):
    with open('./static/bubble.json', 'w') as file:
        jsonf = json.dump(dict, file)

def dictToJSONdata(dict):
    with open('./static/data.json', 'w') as file:
        jsonf = json.dump(dict, file)

def getRepeatedWords(reviews):
    posList = ["NN", "JJ", "VBG", "VB", "NNS", "NNP"]
    wordList = []
    countWords = {}
    mostRepeatedWords = {
        "name": "Most Repeated Words",
        "value": 9999,
        "children": []
    }
    for review in reviews:
        blob = TextBlob(review)
        for word, pos in blob.tags:
            if pos in posList:
                word = word.lower()
                wordList.append(word)

    for word in wordList:
        if word not in countWords.keys():
            countWords[word] = 1
        else:
            countWords[word] += 1

    countWords = sorted(countWords.items(), key=lambda x: x[1], reverse=True)

    for key, value in countWords[:50]:
        wordBlob = TextBlob(key)
        # polarity (from -1 to 1 negative to positive)
        # subjectivity (from 0 to 1, 0 is objective and 1 is subjective)
        score = wordBlob.sentiment.polarity

        mostRepeatedWords['children'].append(
            {"name": key, "value": value, "sentiment": score})

    dictToJSOND3(mostRepeatedWords)
    return mostRepeatedWords


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
        analyzedData['summary'] = 'This restaurant is exellent'
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
        analyzedData['summary'] = 'This restaurant is not bad'
        analyzedData['img'] = 'bad.png'
    else:
        analyzedData['summary'] = "Don't go to this restaurant"
        analyzedData['img'] = 'worse.png'

    return analyzedData


def translate(reviews, language):
    translatedReviews = []

    for review in reviews:
        reviewBlob = TextBlob(review)
        if language == 'th':
            review = reviewBlob.translate(to='th')
        elif language == 'es':
            review = reviewBlob.translate(to='es')
        elif language == 'zh-CN':
            review = reviewBlob.translate(to='zh-CN')
        else:
            review = review
        translatedReviews.append(review)

    return translatedReviews
