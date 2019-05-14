from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response, json
from scrapingFunctions import *
from forms import SearchForm
from sentiment import analyzeReviews, getRepeatedWords, dictToJSONdata, translate
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac4baecbcecee02735c522e42072ede1'

userInput = {}
reviews = []
analyzedData = []
dataDict = {}


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def searchList():

    form = SearchForm(request.form)
    if form.validate_on_submit():
        find = form.find.data
        userInput['find'] = find
        near = form.near.data
        data = getListOfRestaurants(find, near)

        nameList = getListOf(data, 'name')
        reviewCountsList = getListOf(data, 'review_counts')
        urlList = getListOf(data, 'link')

        return render_template('showList.html', title="Restaurant List", find=find, near=near, names_reviews_list=zip(nameList, reviewCountsList, urlList))
    else:
        print(form.errors)
    return render_template('index.html', title='Home', form=form)


@app.route("/reviews", methods=['GET'])
def scrapReviews():
    req = request.args.get('url')
    name = request.args.get('name')
    find = userInput['find']
    userInput['name'] = name
    reviews.clear()
    reviews.append(scrapReviewBundle(req, find))
    dataDict['reviews'] = reviews[0]
    theReviews = reviews[0]
    theWords = getRepeatedWords(theReviews)
    # print(theWords)
    data = analyzeReviews(theReviews)
    analyzedData.clear()
    analyzedData.append(data)
    dataDict['analyzedData'] = analyzedData[0]
    print(dataDict)
    dictToJSONdata(dataDict)


    # print(analyzedData)
    return render_template('reviews.html', title="Reviews", theLink=userInput, reviews=theReviews, data=data, name=name, theWords=theWords)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/bubble")
def bubble():
    name = userInput['name']
    print(name)
    return render_template('bubble.html', title="Bubble Chart", name=name)


@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")


def JSONtoDict():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/", "data.json")
    data = json.load(open(json_url))
    return data


@app.route("/translate", methods=['GET'])
def lang():
    # theReviews = reviewsDict['reviews']
    # print(theReviews)
    data = JSONtoDict()
    theReviews = data['reviews']
    theInput = userInput
    lang = request.args.get('lang')
    newReviews = translate(theReviews, lang)
    # data = reviewsDict['analyzedData']
    theData = data['analyzedData']
    # print(analyzedData)
    return render_template('lang.html', title="Translation", reviews=newReviews, theInput=theInput, data=theData)


if __name__ == '__main__':
    app.run(debug=True)
