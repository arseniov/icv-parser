# icv_collections_parser.py
import os
import requests
from bs4 import BeautifulSoup
from icv_database import create_table, insert_links
from icv_login import icv_login

def icv_collections_parsing(collection_url, table_name):
    # Check if the ./data/session_cookie.txt file exists
    if not os.path.exists('./data/session_cookie.txt'):
        print("Session cookie file not found. Running login script.")
        icv_login()  # Run the login script to get the ./data/session_cookie.txt file
        
    # Load cookies from the file
    with open('./data/session_cookie.txt', 'r') as file:
        cookies_str = file.read()

    # Convert the cookies string to a dictionary
    cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_str.split('\n') if cookie}

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '; '.join([f'{key}={value}' for key, value in cookies.items()]),
        'Host': 'www.icv-crew.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    all_links = set()

    # Loop through all collection URLs
    for url in collection_url:
        # Make the authenticated GET request
        response = requests.get(url, headers=headers)

        # Check if the class "button_submit" is found in the HTML page
        soup = BeautifulSoup(response.text, 'html.parser')
        button_submit = soup.find(class_='button_submit')

        if button_submit is None:
            print(f"User is authenticated. Parsing page: {url}")

            # Extract information from "td" elements with class "tlistcol2"
            td_elements = soup.find_all('td', class_='tlistcol2')
            for td in td_elements:
                a_element = td.find('a')
                if a_element:
                    href = a_element.get('href')
                    inner_text = a_element.get_text(strip=True)
                    all_links.add((href, inner_text))
        else:
            print("User is not authenticated. Logging in and retrying the request.")
            icv_login()  # Call the login function to refresh the authentication
            all_links.update(icv_collections_parsing([url], table_name))  # Retry the original GET request

    return all_links
    
    pass

if __name__ == "__main__":

    # Loop through each collection URL and table name
    for table_name, urls in collection_urls.items():
        # Create the table in the database
        create_table(table_name)

        # Get all links and their inner text for the specific collection
        all_links = icv_collections_parsing(urls, table_name)

        # Insert all links into the corresponding table
        insert_links(table_name, all_links)
        
        pass
