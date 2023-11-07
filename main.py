from amaz_scrappy import amaz_by_name
from flip_scrapper import flip_by_name
from tabulate import tabulate
import textwrap

def main():
    try:
        # Define the product name and the number of results you want
        product_name = input("Enter the product name: ")
        n_search = 5
        print()

        # Print a message to let the user know that the data is being fetched
        print("Hold on while we fetch the data...")

        # Fetch data from Amazon and Flipkart
        amazon_data = amaz_by_name(product_name, n_search)
        flipkart_data = flip_by_name(product_name, n_search)

        # Combine data from Amazon and Flipkart into a single list
        combined_data = amazon_data + flipkart_data

        # Sort the data by price in non-decreasing order
        sorted_data = sorted(combined_data, key=lambda x: x['price'])

        # Create a list of lists to hold the data
        table_data = []

        # Format the data and add rows to the table data
        for item in sorted_data:
            title = item['title']
            price = item['price']
            rating = item['rating']
            link = item['link']

            # Wrap the title and link to specified widths
            title = '\n'.join(textwrap.wrap(title, width=30))
            link = '\n'.join(textwrap.wrap(link, width=60))

            table_data.append([title, price, rating, link])

        # Define the table headers
        headers = ["Title", "Price (₹)", "Rating", "Link"]

        # Generate the formatted table with the adjusted column width using the "grid" format
        table = tabulate(table_data, headers, tablefmt="fancy_grid", stralign="left", colalign=("left", "center", "center", "left"), numalign="center")

        # Print the table in the terminal
        print(table)

        print()

        #print the most economical product
        print("The most economical product is:")
        print(f"Title: {sorted_data[0]['title']}")
        print(f"Price: ₹{sorted_data[0]['price']}")
        print(f"Rating: {sorted_data[0]['rating']}")
        print(f"Link: {sorted_data[0]['link']}")
        print()
        print("Choose the product that suits you the best!")
        print("Thank you for using our service!")
        print()


    except ConnectionError:
        print("Error: Unable to establish a connection. Please check your internet connection.")
    except Exception as e:
        print(f"An error occurred while fetching data.\n Please try again")

if __name__ == "__main__":
    main()
