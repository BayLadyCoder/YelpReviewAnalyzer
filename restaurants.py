from beautifulSoupUtils import runBeautifulSoup

# ------- Home/Search Page ------- #
# searchURL = "https://www.yelp.com/search?find_desc=thai%20food&find_loc=owings%20mills"
# example = "https://www.yelp.com/search?find_desc=sushi&find_loc=baltimore"

# find url that have list of restaurants from the user search input
def searchListURL(find, near):
    Yelp = "https://www.yelp.com/search?find_desc="
    what = find.replace(' ', '%20')
    where = '&find_loc=' + near.replace(' ', '%20')
    searchURL = Yelp + what + where
    return searchURL


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


# bundle functions for Flask after get user input (find and near)
def getListOfRestaurants(find, near):
    # url = searchListURL(find, near)
    url = 'http://127.0.0.1:5500/index.html'

    # soup = runBeautifulSoup(url)
    # totalListPages = findTotalRestaurantListPages(soup)
    # data = scrapRestaurantList(url, totalListPages)

    return scrapRestaurantList(url)


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


