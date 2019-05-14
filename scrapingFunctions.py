import requests
from bs4 import BeautifulSoup
import json

# ------- Home Page ------- #
# searchURL = "https://www.yelp.com/search?find_desc=thai%20food&find_loc=owings%20mills"
# example = "https://www.yelp.com/search?find_desc=sushi&find_loc=baltimore"

#Get user input
def TESTgetUserInput():
    userInput = {}
    find = input('What kind of food you are looking for: ')
    near = input('Location: ')
    userInput['find'] = find
    userInput['near'] = near
    return userInput


# find url from the user search input
def TESTsearchListURL(userInput):
    Yelp = "https://www.yelp.com/search?find_desc="
    what = userInput['find'].replace(' ', '%20')
    where = '&find_loc=' + userInput['near'].replace(' ', '%20')
    searchURL = Yelp + what + where
    # print(searchURL)
    return searchURL

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
def scrapRestaurantList(link, totalListPages):
    page = 1
    startAt = 0
    data = []
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
    print(url)
    soup2 = runBeautifulSoup(url)

    for div in soup2.find_all('div', class_="mainAttributes__373c0__1r0QA"):
        restaurant = {}
        for h3 in div.findChildren('h3', class_="alternate__373c0__1uacp"):
            for a in h3.findChildren('a'):
                restaurant['name'] = a.text
                restaurant['link'] = a.get('href')
        if(div.findChildren('span', class_="reviewCount__373c0__2r4xT")):
            for span in div.findChildren('span', class_="reviewCount__373c0__2r4xT"):
                restaurant['review_counts'] = int(span.text[:-7])
        else:
            restaurant['review_counts']  = 0
        data.append(restaurant)

    page += 1

    return data


# bundle functions for Flask after get user input (find and near)
def getListOfRestaurants(find, near):
    url = searchListURL(find, near)
    soup = runBeautifulSoup(url)
    totalListPages = findTotalRestaurantListPages(soup)
    data = scrapRestaurantList(url, 1)
    return data


# get a list of all restaurants' names, links, or review_counts
def getListOf(data, getThis):
    listAll = []
    for i in range(len(data))[1:]:
        listAll.append(data[i][getThis])
    return listAll

# Print all names of the places and the numbers of reviews
# with their index number for the user to choose
def TESTprintNamesAndReviews(listNames, listReviews):
    index = 1
    for name, reviews in zip(listNames, listReviews):
        if reviews <= 1:
            print(index, name, reviews, "review")  
        else:
            print(index, name, reviews, "reviews")  
        index+=1  

# get a specific link (when user choose a restaurant)
def TESTgetTheLink(allInfo, index):
    index = index -1
    print(allInfo[index]['link'])
    return allInfo[index]['link'] 

# ---------------------------------------------------------------------------------------

# ------- Create URL of the Reviews Page (The Chosen Restaurant Page) ------- #
def createThePlaceURL(link, find):
    # example = "https://www.yelp.com/biz/baltimore-built-bistro-b3-baltimore-3?start=1"
    Yelp = "https://www.yelp.com"
    print("find = ", find)
    toBeRemoved = -(len(find)+5)
    print(toBeRemoved)
    print(link)
    link = link[:toBeRemoved]
    start1 = "?start=1"
    url = Yelp+link+start1
    print(url)
    return url

# find total (reviews) pages to scrape all reviews 
def findTotalReviewPages(soup):
    totalPages = ''
    for div in soup.find_all('div', class_="page-of-pages"):
        pageOfPages = div.text.strip()
        totalPages = pageOfPages[10:]
        totalPages = int(totalPages)
    return totalPages

 # Scraping all reviews
def scrapeReviews(link, totalPages):
    allReviews = []
    link = link[:-1]
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
        url = link+strStartAt
        pageOfPages = "(Page " + str(page) + " of " + str(totalPages) + ")"
        print(url, pageOfPages)
        soup = runBeautifulSoup(url)
        # print all reviews
        for p in soup.find_all('p', {"lang": "en"}):
            # print(countReviews)
            review = p.text
            # print(review, '\n')
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


def TESTprintAllReviews(reviewsList):
    i = 1
    print(len(reviewsList))
    for review in reviewsList:
        print(i, '\n', review, '\n')
        i+=1

# create JSON file from Python Dictionary ()
# def pythonToJSON(listOfDict):
#     with  open('new_list.json', 'w') as f:
#         json.dump(listOfDict, f)


def scrapReviewBundle(link, find):
    url = createThePlaceURL(link, find)
    soup = runBeautifulSoup(url)
    pages = findTotalReviewPages(soup)
    reviews = scrapeReviews(url, pages)
    return reviews



# This was for testing all the functions before I started Flask
# It doesn't work anymore since I changed some code inside many functions
# to make it work for Flask
def TESTstart():
    # Get user input
    userInput = TESTgetUserInput()

    # Get search URL (List of restaurants/Places Page)
    listURL = TESTsearchListURL(userInput)

    # created BeautifulSoup object
    soup1 = runBeautifulSoup(listURL)

    totalListPages = findTotalRestaurantListPages(soup1)

    # get all 'info' (names, links(href), and numbers of reviews)
    # (scrape the 'info' of the places in the list, then store them into a list
    # the list can be different, based on user input)
    info = scrapRestaurantList(listURL, totalListPages)

    print(info)
    listNames = getListOf(info, "name")
    listReviews = getListOf(info, "review_counts")

    # Print all names and numbers of reviews for user to choose
    printNamesAndReviews(listNames, listReviews)

    # User choose a place to find its reviews
    chosenPlace = int(input(
        "Enter the 'number' of the restaurant you want to see reviews: "))

    # # get the href link from that chosen place
    theLink = getTheLink(info, chosenPlace)

    # # create real/working url
    thePlaceURL = createThePlaceURL(theLink, userInput)

    # # create Beautiful Soup object
    soup2 = runBeautifulSoup(thePlaceURL)

    # # find Total pages of reviews
    totalPages = findTotalReviewPages(soup2)

    # # scraping all reviews from all the pages (return a list of all reviews)
    allReviews = scrapeReviews(thePlaceURL, totalPages)

    outputToTextFile(allReviews)

    return allReviews


# -------------------------------------------------------------------------------------
# ------------------ Program starts here -------------------
# TESTING
# allReviews = scrapeReviews("https://www.yelp.com/biz/fuji-yama-sushi-bar-reisterstown?start=1", 3)
# outputToTextFile(allReviews)
# pythonToJSON(allReviews)
