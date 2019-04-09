from flask import Flask, render_template, request
from YelpScrapingDict import *



app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    # reviews = start()
    return render_template('index.html')

@app.route("/search")
def search_page():
    return render_template('search.html')

@app.route("/search", methods=['POST'])
def search():
    find = request.form['find']
    near = request.form['near']
    return render_template('searchAgain.html', find = find, near=near)

@app.route("/search-again")
def searchAgain():
    return render_template('searchAgain.html', title="Search Again")


@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")

if __name__ == '__main__':
    app.run(debug=True)