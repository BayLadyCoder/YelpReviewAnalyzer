from textblob import TextBlob
from jsonUtils import dictToJSOND3

def prepareMostRepeatedWords(reviews):
    posList = ["NN", "JJ", "VBG", "VBP", "NNS"]
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

    for key, value in countWords[:30]:
        wordBlob = TextBlob(key)
        # polarity (from -1 to 1 negative to positive)
        # subjectivity (from 0 to 1, 0 is objective and 1 is subjective)
        score = wordBlob.sentiment.polarity

        mostRepeatedWords['children'].append(
            {"name": key, "value": value, "sentiment": score})

    dictToJSOND3(mostRepeatedWords)
    return mostRepeatedWords

