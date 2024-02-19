import requests
from bs4 import BeautifulSoup
import json

# ------- Home Page ------- #
# searchURL = "https://www.yelp.com/search?find_desc=thai%20food&find_loc=owings%20mills"
# example = "https://www.yelp.com/search?find_desc=sushi&find_loc=baltimore"

# find url that have list of restaurants from the user search input
def searchListURL(find, near):
    Yelp = "https://www.yelp.com/search?find_desc="
    what = find.replace(' ', '%20')
    where = '&find_loc=' + near.replace(' ', '%20')
    searchURL = Yelp + what + where
    return searchURL

# get code and build BeautifulSoup object
def runBeautifulSoup(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

# find total pages of the list of restaurant
def findTotalRestaurantListPages(soup):
    totalPages = ''     
    for div in soup.find_all('div', {'role':'navigation'}):
        for span in div.find_all("span", {'class':["lemon--span__373c0__3997G", "text__373c0__2pB8", "text-color--normal__373c0__K_MKN", "text-align--left__373c0__2pnx_"]}):
            if "Page" in span.text:
                #print(span.text)
                pageOfPages = span.text.strip()
                totalPages = pageOfPages[10:]
                #print(totalPages)
                totalPages = int(totalPages)
            
    return totalPages

# Get a list of restaurants, their links(url), and numbers of reviews based on user searching input
def scrapRestaurantList(link, totalListPages = 1):
    page = 1
    startAt = 0
    data = []
    restaurants = {};
    # I commented out this below code because I only want to print list from the first page only
    # Otherwise it will take too much time and too many options for user (for now)

    # if totalListPages > 2:
    #     totalListPages = 2
    # startAt = start at restaurant number(1,30,60,90) this is for the url
    # while page <= totalListPages:
    #     if page == 1:
    #         url = link
    #     elif page > 1:
    #         startAt = (page-1)*30
    #         strStartAt = str(startAt)
    #         url = link+strStartAt
    #     pageOfPages = "(Page " + str(page) + " of " + str(totalListPages) + ")"
    #     print(url, pageOfPages)
    url = link
    print(f"restaurant list url: {url}")
    soup2 = runBeautifulSoup(url)

    for div in soup2.find_all('div', class_="css-1qn0b6x"):
        span = div.select_one(".css-chan6m")
        h3 = div.select_one("h3.css-1agk4wl")
   
        if h3 == None or span == None:
            continue
    
        a = h3.find('a',{'class':'css-19v1rkv'})

        restaurant = {"name": a.text, "link": a.get('href')}
        
        if restaurant.get('name') != "" and restaurant.get('link') != "" and span.text != '--:--':
            totalReviews = span.text.split(' ')[0][1:]
            if totalReviews[-1] == 'k': 
                totalReviews = float(totalReviews[:-1]) * 1000;
            else:    
                totalReviews = int(totalReviews)
            restaurant['review_counts'] = totalReviews
            restaurants[restaurant.get('name')] = restaurant;
        
    page += 1

    for attr, value in restaurants.items():
        data.append(value)


    return data


# bundle functions for Flask after get user input (find and near)
def getListOfRestaurants(find, near):
    # url = searchListURL(find, near)
    url = 'http://127.0.0.1:5500/index.html'

    # soup = runBeautifulSoup(url)
    # totalListPages = findTotalRestaurantListPages(soup)
    # data = scrapRestaurantList(url, totalListPages)

    return scrapRestaurantList(url)

# get a list of all restaurants' names, links, or review_counts
def getListOf(data, key):
    listAll = []
    for restaurant in data:
        listAll.append(restaurant[key])
    return listAll

# ------- Create URL of the Reviews Page (The Chosen Restaurant Page) ------- #
def createThePlaceURL(link, find):
    # example = "https://www.yelp.com/biz/baltimore-built-bistro-b3-baltimore-3?start=1"
    Yelp = "https://www.yelp.com"
    start1 = "?start=1"
    # url = Yelp+link+start1
    # return url
    return Yelp+link

# find total (reviews) pages to scrape all reviews 
def findTotalReviewPages(soup):
    totalPages = ''
    span = soup.find('div', class_='css-1aq64zd').find('span',class_='css-chan6m')

    totalPages = span.text.split(' of ')[1]
    totalPages = int(totalPages)
    return 1
    # return totalPages

 # Scraping all reviews
def scrapeReviews(link, totalPages = 1):
    allReviews = []
    # link = link[:-1]
    page = 1
    countReviews = 1
    startAt = 1
    # startAt = start at review number(1,20,40,60,80) this is for the url
    while page <= totalPages:
        if page == 1:
            startAt = 1
        elif page > 1:
            startAt = (page-1)*20
        strStartAt = str(startAt)
        # url = link+strStartAt
        # pageOfPages = "(Page " + str(page) + " of " + str(totalPages) + ")"
        pageOfPages = 1
        url = link
        print(url, pageOfPages)
        soup = runBeautifulSoup(url)
        for span in soup.find_all('span', {"lang": "en"}):
            review = span.text
            allReviews.append(review)
            countReviews += 1
        page += 1
    return allReviews

def TESToutputToTextFile(reviewList):
    fileName = "theReviews.txt"
    file = open(fileName, 'w')
    for review in reviewList:
        file.write(review)
        file.write('\n')

    file.close()

# create JSON file from Python Dictionary ()
# def pythonToJSON(listOfDict):
#     with  open('new_list.json', 'w') as f:
#         json.dump(listOfDict, f)

def scrapReviewBundle(link, find):
    # url = createThePlaceURL(link, find)
    url = 'http://127.0.0.1:5500/reviewPage.html'
    soup = runBeautifulSoup(url)
    pages = findTotalReviewPages(soup)
    reviews = scrapeReviews(url, pages)
    return reviews
