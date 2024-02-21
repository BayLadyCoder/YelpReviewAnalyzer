from beautifulSoupUtils import runBeautifulSoup

# ------- Create URL of the Reviews Page (The Chosen Restaurant Page) ------- #
def createThePlaceURL(link):
    # example = "https://www.yelp.com/biz/baltimore-built-bistro-b3-baltimore-3?start=1"
    Yelp = "https://www.yelp.com"
    start1 = "?start=1"
    # url = Yelp+link+start1
    # return url
    return Yelp+link

# find total (reviews) pages to scrape all reviews 
def findTotalReviewPages(url):
    totalPages = 1
    span = runBeautifulSoup(url).find('div', class_='css-1aq64zd').find('span',class_='css-chan6m')
    totalPages = span.text.split(' of ')[1]
    totalPages = int(totalPages)

    if(totalPages > 2):
        return 2
    else:
        return totalPages

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
        url = link+strStartAt
        pageOfPages = "(Page " + str(page) + " of " + str(totalPages) + ")"
        # pageOfPages = 1
        # url = link
        # print(url, pageOfPages)
        soup = runBeautifulSoup(url)
        for span in soup.find_all('span', {"lang": "en"}):
            review = span.text
            allReviews.append(review)
            countReviews += 1
        page += 1
    return allReviews

def getReviews(urlPath):
    url = createThePlaceURL(urlPath)
    # url = 'http://127.0.0.1:5500/reviewPage.html'
    totalPages = findTotalReviewPages(url)
    return scrapeReviews(url, totalPages)
