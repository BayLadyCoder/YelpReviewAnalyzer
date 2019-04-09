import requests
from bs4 import BeautifulSoup


# ------- Home Page ------- #
# searchURL = "https://www.yelp.com/search?find_desc=thai%20food&find_loc=owings%20mills"
# example = "https://www.yelp.com/search?find_desc=sushi&find_loc=baltimore"

# Get user input
def getUserInput():
    userInput = []
    find = input('What kind of food you are looking for: ')
    near = input('Location: ')
    userInput.append(find)
    userInput.append(near)
    return userInput

# find url from the user search input
def searchListURL(userInput):
    Yelp = "https://www.yelp.com/search?find_desc="
    what = userInput[0].replace(' ', '%20')
    where = '&find_loc=' + userInput[1].replace(' ', '%20')
    searchURL = Yelp + what + where
    # print(searchURL)
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
    restaurants = []
    links = []
    reviews = []
    info = []
    # startAt = start at restaurant number(1,30,60,90) this is for the url
    while page <= totalListPages:
        if page == 1:
            url = link
        elif page > 1:
            startAt = (page-1)*30
            strStartAt = str(startAt)
            url = link+strStartAt
        pageOfPages = "(Page " + str(page) + " of " + str(totalListPages) + ")"
        print(url, pageOfPages)
        soup2 = runBeautifulSoup(url)

        for div in soup2.find_all('div', class_="mainAttributes__373c0__1r0QA"):
            for h3 in div.findChildren('h3', class_="alternate__373c0__1uacp"):
                for a in h3.findChildren('a'):
                    restaurant = a.text
                    href = a.get('href')
                    restaurants.append(restaurant)
                    links.append(href)
            if(div.findChildren('span', class_="reviewCount__373c0__2r4xT")):
                for span in div.findChildren('span', class_="reviewCount__373c0__2r4xT"):
                    review = span.text
                    reviews.append(review)
            else:
                review = "0 review"
                reviews.append(review)
        page += 1

    info.append(restaurants)
    info.append(links)
    info.append(reviews)

    return info


# print all restaurants' names and their links
def printAllInfo(info):
    i = 0
    while i < len(info):
        j = 1
        while j < len(info[i]):
            print(info[i][j])
            print()
            j += 1
        i += 1

# get all the links from user search input
def getAllLinks(info):
    j = 1
    links = []
    while j < len(info[1]):
        print(info[1][j])
        links.append(info[1][j])
        j += 1
    return links

# get all restaurants' names from user search input
def getAllNames(info):
    j = 1
    names = []
    while j < len(info[0]):
        print(j, info[0][j])
        names.append(info[1][j])
        j += 1
    return names

# get a specific link (when user choose a restaurant)
def getTheLink(info, index):
    print(info[1][index])
    return info[1][index]

# get a specific name of a restaurant (chosen restaurant)
def getTheName(info, index):
    print(info[0][index])
    return info[0][index]


# Print all names of the places and the numbers of reviews
# with their index number for the user to choose
def printNamesAndReviews(info):
    j = 1
    while j < len(info[0]):
        number = str(j)+"."
        review = info[2][j]
        reviews = "("+review+")"
        print(number, info[0][j], reviews)
        j += 1


# ---------------------------------------------------------------------------------------

# ------- Get the Reviews Page (The Chosen Restaurant Page) ------- #
def createThePlaceURL(link, userInput):
    # example = "https://www.yelp.com/biz/baltimore-built-bistro-b3-baltimore-3?start=1"
    Yelp = "https://www.yelp.com"
    find = userInput[0]
    toBeRemoved = -(len(find)+5)

    # print(toBeRemoved)
    link = link[:toBeRemoved]
    start1 = "?start=1"
    url = Yelp+link+start1
    print(url)
    return url

# find total pages (reviews)
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


def printAllReviews(reviewsList):
    i = 1
    print(len(reviewsList))
    for review in reviewsList:
        print(i, '\n', review, '\n')
        i+=1

def start():
    # Get user input
    userInput = getUserInput()

    # Get search URL (List of restaurants/Places Page)
    listURL = searchListURL(userInput)

    # created BeautifulSoup object
    soup1 = runBeautifulSoup(listURL)

    totalListPages = findTotalRestaurantListPages(soup1)

    # get all 'info' (names, links(href), and numbers of reviews)
    # (scrape the 'info' of the places in the list, then store them into a list
    # the list can be different, based on user input)
    info = scrapRestaurantList(listURL, totalListPages)

    # Print all names and numbers of reviews for user to choose
    printNamesAndReviews(info)

    # User choose a place to find its reviews
    chosenPlace = int(input(
        "Enter the 'number' of the restaurant you want to see reviews: "))

    # get the href link from that chosen place
    theLink = getTheLink(info, chosenPlace)

    # create real/working url
    thePlaceURL = createThePlaceURL(theLink, userInput)

    # create Beautiful Soup object
    soup2 = runBeautifulSoup(thePlaceURL)

    # find Total pages of reviews
    totalPages = findTotalReviewPages(soup2)

    # scraping all reviews from all the pages (return a list of all reviews)
    allReviews = scrapeReviews(thePlaceURL, totalPages)

    # print all reviews
    printAllReviews(allReviews)
    #print(allReviews)

    return (info, allReviews)

# -------------------------------------------------------------------------------------
# ------------------ Program starts here -------------------
info, allReviews = start()
