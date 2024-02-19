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
    dictToJSONdata({"reviews": reviews, "analyzedData": analyzedData})

    return render_template('reviews.html', title="Reviews", reviews=reviews, data=analyzedData, name=name)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/bubble")
def bubble():
    return render_template('bubble.html', title="Bubble Chart", name=userInput['name'])


@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")


def JSONtoDict():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/", "data.json")
    return json.load(open(json_url))


@app.route("/translate", methods=['GET'])
def translateReviews():
    data = JSONtoDict()
    reviews = data['reviews']
    language = request.args.get('lang')

    return render_template('lang.html', title="Translation", reviews=translate(reviews, language), name=userInput['name'], data=data['analyzedData'])


if __name__ == '__main__':
    app.run(debug=True)
