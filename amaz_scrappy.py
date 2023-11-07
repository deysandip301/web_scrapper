import requests
from bs4 import BeautifulSoup


#User-Agent header to pretend as a browser
headers = {
'authority': 'www.google.in',
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

def amaz_by_name(product_name,n_search=5):
    
    #Creating amazon items list
    amazon_item_list = []

    # creating the amazon search link
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    headers['authority'] = 'www.amazon.in'


    # Get the Amazon page content and parse it with BeautifulSoup
    count = 1
    amazon_response = requests.get(amazon_url, headers=headers)
    while(amazon_response.status_code != 200 and count!=20):
        amazon_response = requests.get(amazon_url, headers=headers)
    
    #parse the response
    amazon_soup = BeautifulSoup(amazon_response.text, 'html.parser')

    # Get the product details in a list view
    for product in amazon_soup.find_all('div', {'class': 's-result-item'}) :
        if(count>n_search):
            break

        #get the title and price
        amazon_title = product.find('span', {'class': 'a-text-normal'})
        amazon_price = product.find('span', {'class': 'a-price-whole'})
        if(amazon_title == None or amazon_price == None):
            continue
        amazon_title = amazon_title.text.strip()
        amazon_price = amazon_price.text.strip()
        amazon_price = float(amazon_price.replace(",", ""))

        # if the price is 0, skip the product
        if (amazon_price == 0) :
            continue

        #get the rating
        amazon_rating = product.find('span', {'class': 'a-icon-alt'})
        if amazon_rating != None:
            amazon_rating = amazon_rating.text.strip()
            amazon_rating = amazon_rating.replace(" ", "⭐ ", 1)
            amazon_rating = amazon_rating.replace(" out of 5 stars", " / 5 stars")
        else :
            amazon_rating = "No rating"
        

        if amazon_rating == None:
            amazon_rating = "No rating"

        #get the product link
        amazon_link = product.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        amazon_link = f"https://www.amazon.in{amazon_link}"


        #append the details to the list
        amazon_item_list.append({
            'title': amazon_title,
            'price': amazon_price,
            'rating': amazon_rating,
            'link' : amazon_link
        })
        count += 1

        # Get the product details in a grid view
    for product in amazon_soup.find_all('div', {'class': 'sg-col-inner'}) :
        if(count>n_search):
            break

        # Get the title
        amazon_title = product.find('span', {'class': 'a-size-base-plus a-color-base'})
        if(amazon_title == None):
            amazon_title = product.find('span', {'class' : 'a-size-base-plus a-color-base a-text-normal'})
        amazon_title_2 = product.find('span', {'class' : 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
        if(amazon_title_2 != None):
            amazon_title += amazon_title_2
        
        # Get the price
        amazon_price = product.find('span', {'class': 'a-offscreen'})
        if(amazon_title == None or amazon_price == None):
            continue
        amazon_title = amazon_title.text.strip()
        amazon_price = amazon_price.text.strip()
        amazon_price = amazon_price.replace("₹", "")
        amazon_price = float(amazon_price.replace(",", ""))

        # If the price is 0, skip the product
        if (amazon_price == 0) :
            continue

        # Get the rating
        amazon_rating = product.find('span aria-label')
        if(amazon_rating == None):
            amazon_rating = product.find('span', {'class': 'a-icon-alt'})
        if amazon_rating != None:
            amazon_rating = amazon_rating.text.strip().replace(" ", "⭐ ", 1)
            amazon_rating = amazon_rating.replace(" out of 5 stars", " / 5 stars")

        if amazon_rating == None:
            amazon_rating = "No rating"

        # Get the product link
        amazon_link = product.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        amazon_link = f"https://www.amazon.in{amazon_link}"
        if amazon_link == None:
            amazon_link = product.find('a', {'class': 'a-link-normal a-text-normal'})['href']
            amazon_link = f"https://www.amazon.in{amazon_link}"
        if amazon_link == None:
            amazon_link = ""
        
        #append the details to the list
        amazon_item_list.append({
            'title': amazon_title,
            'price': amazon_price,
            'rating': amazon_rating,
            'link' : amazon_link
        })
        count += 1

    return amazon_item_list

if __name__ == "__main__":

    product_name = input("Enter product name : ")
    print()
    search_results = amaz_by_name(product_name, 5)
    for i, result in enumerate(search_results, 1):
        print(f"Result {i}:")
        print(f"Title: {result['title']}")
        print(f"Price: ₹{result['price']}")
        print(f"Rating: {result['rating']}")
        print(f"Link: {result['link']}")
        print()
    







        

