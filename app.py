from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response, json
from scrapingFunctions import *
from forms import SearchForm
from sentiment import analyzeReviews, getRepeatedWords, dictToJSONdata, translate
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac4baecbcecee02735c522e42072ede1'

userInput = {}


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def searchRestaurantList():
    form = SearchForm(request.form)
    if form.validate_on_submit():
        near = form.near.data
        find = form.find.data

        return render_template('showList.html', title="Restaurant List", find=find, near=near, restaurants=getListOfRestaurants(find, near))
    else:
        print(form.errors)
    return render_template('index.html', title='Home', form=form)


@app.route("/reviews", methods=['GET'])
def analyzedReviews():
    urlPath = request.args.get('url')
    name = request.args.get('name')
    userInput['name'] = name
    reviews = getReviews(urlPath)
    analyzedData = analyzeReviews(reviews)
    dictToJSONdata(analyzedData)

    return render_template('reviews.html', title="Reviews", theLink=userInput, reviews=reviews, data=analyzedData, name=name, theWords=getRepeatedWords(reviews))


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/bubble")
def bubble():
    name = userInput['name']
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
