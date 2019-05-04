from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
from YelpScrapingDict import *
from forms import SearchForm
from jsonToPy import orders

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac4baecbcecee02735c522e42072ede1'

userInput = {}

# 1. store "find" variable global because need to use it again for 
# for function createThePlaceURL
# for scraping reviews to analyze

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

        return render_template('showList.html', title="Restaurant List", find = find, near=near, names_reviews_list = zip(nameList,reviewCountsList, urlList))
    else:
        print(form.errors)
    return render_template('index.html', title='Home', form=form)



@app.route("/reviews", methods=['POST', 'GET'])
def reviews():

    if request.method == 'POST':
        req = request.get_json()
        link = req['link']
        # theLink.clear()
        # theLink.append(req['link'])
        userInput['link'] = link

        # print("data is: (POST)", req)  
        print("link is: (POST)", userInput)  
      

    else:    
        print('link is: (GET)', userInput['link'])
        return render_template('reviews.html', title="Reviews", theLink = userInput )


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/api/orders", methods=['GET', 'POST'])
def api():
    return render_template('api.html', title="API", orders=orders)


@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")


if __name__ == '__main__':
    app.run(debug=True)
