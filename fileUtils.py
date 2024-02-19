def createSearchRestaurantsFileName (find, near):
    filePath = './static/database/searches/'
    fileName = '-'.join(find.lower().split(' ')) + '-' + '-'.join(near.lower().split(' '))
    return filePath + fileName;

def createRestaurantReviewsFileName (name):
    filePath = './static/database/reviews/'
    fileName = '-'.join(name.lower().split(' ')) + "-reviews" 
    return filePath + fileName