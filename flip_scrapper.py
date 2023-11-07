import requests
from bs4 import BeautifulSoup

#User-Agent header to pretend as a browser
headers = {
'authority': 'www.flipkart.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def flip_by_name(product_name,n_search=5):

    #Creating flipkart items list
    flipkart_item_list = []

    # creating the flipkart search link
    flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
    headers['authority'] = 'www.flipkart.com'

    # Get the flipkart page content and parse it with BeautifulSoup
    count = 1
    flipkart_response = requests.get(flipkart_url, headers=headers)
    while(flipkart_response.status_code != 200 and count!=20):
        flipkart_response = requests.get(flipkart_url, headers=headers)
    
    #parse the response
    flipkart_soup = BeautifulSoup(flipkart_response.text, 'html.parser')

    # Get the product details in a list view
    for product in flipkart_soup.find_all('div', {'class': '_2kHMtA'}) :
        if(count>n_search):
            break

        #get the title and price
        flipkart_title = product.find('div', {'class': '_4rR01T'})
        flipkart_price = product.find('div', {'class': '_30jeq3 _1_WHN1'})
        if(flipkart_title == None or flipkart_price == None):
            continue
        flipkart_title = flipkart_title.text.strip()
        flipkart_price = flipkart_price.text.strip()
        flipkart_price = flipkart_price[1:] # remove the ₹ symbol
        flipkart_price = float(flipkart_price.replace(",", ""))

        # if the price is 0, skip the product
        if (flipkart_price == 0) :
            continue

        #get the rating
        flipkart_rating = product.find('div', {'class': '_3LWZlK'}).text.strip()
        flipkart_rating = f"{flipkart_rating} ⭐ / 5 stars"

        if flipkart_rating == None:
            flipkart_rating = "No rating"

        #get the product link
        flipkart_link = "https://www.flipkart.com" + product.find('a', {'class': '_1fQZEK'})['href']

        flipkart_item_list.append({
            'title': flipkart_title,
            'price': flipkart_price,
            'rating': flipkart_rating,
            'link' : flipkart_link
        })
        count += 1
    
    # get the product details in a grid view
    for product in flipkart_soup.find_all('div', {'class': '_1AtVbE col-12-12'}) :
        if(count>n_search):
            break

        #get the title and link
        flipkart_title = product.find('div', {'class': '_2WkVRV'})
        
        if (flipkart_title == None):
            flipkart_title = product.find('a', {'class': 's1Q9rs'})
        flipkart_title_2 = product.find('a', {'class': 'IRpwTa'})
        

        # Get the price
        flipkart_price = product.find('div', {'class': '_30jeq3'})
        if(flipkart_title == None or flipkart_price == None):
            continue
        if flipkart_title_2 != None:
            flipkart_link = "https://www.flipkart.com" + flipkart_title_2['href']
        else:
            flipkart_link = "https://www.flipkart.com" + flipkart_title['href']

        flipkart_title = flipkart_title.text.strip()
        if flipkart_title_2 != None:
            flipkart_title = flipkart_title +" " + flipkart_title_2.text.strip()
        flipkart_price = flipkart_price.text.strip()
        flipkart_price = flipkart_price[1:] # remove the ₹ symbol
        flipkart_price = float(flipkart_price.replace(",", ""))

        # if the price is 0, skip the product
        if (flipkart_price == 0) :
            continue



        #get the rating
        flipkart_rating = product.find('div', {'class': '_3LWZlK'})
        if flipkart_rating == None:
            flipkart_rating = "No rating"
        else :
            flipkart_rating = flipkart_rating.text.strip()
            flipkart_rating = f"{flipkart_rating}⭐ / 5 stars"

        # handling the product link
        if flipkart_link == None:
            flipkart_link = ""

        flipkart_item_list.append({
            'title': flipkart_title,
            'price': flipkart_price,
            'rating': flipkart_rating,
            'link' : flipkart_link
        })
        count += 1
    
    return flipkart_item_list



if __name__ == "__main__":

    product_name = input("Enter product name : ")
    print()
    search_results = flip_by_name(product_name, 5)
    i = 1
    for result in search_results:
        print(f'Item {i} :')
        print(f'Title : {result["title"]}')
        print(f'Price : {result["price"]}')
        print(f'Rating : {result["rating"]}')
        print(f'Link : {result["link"]}')
        print()
        i+=1