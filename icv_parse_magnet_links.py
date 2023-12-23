import sys
import requests
from bs4 import BeautifulSoup

def load_cookies(cookie_file='./data/session_cookie.txt'):
    with open(cookie_file, 'r') as file:
        cookies_str = file.read()
    return {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_str.split('\n') if cookie}

def make_authenticated_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        thank_you_button_link = soup.find('a', class_='thank_you_button_link')

        if thank_you_button_link:
            response = requests.get(thank_you_button_link['href'], headers=headers)
            # Wait for redirection/page refresh (You may need to implement additional logic here based on the website behavior)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

        return soup
    except requests.RequestException as e:
        print(f"Error making authenticated request: {e}")
        return None

def extract_magnet_links(soup):
    magnet_links = []
    a_elements = soup.find_all('a', href=True)
    for a_element in a_elements:
        if a_element['href'].startswith('magnet:'):
            magnet_links.append((a_element['href'], a_element.string))
    return magnet_links

def parse_magnet_links(link_url):
    cookies = load_cookies()
    
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

    soup = make_authenticated_request(link_url, headers)

    if soup:
        magnet_links = extract_magnet_links(soup)
        return magnet_links
    else:
        return []

if __name__ == "__main__":
    # Get the link_url from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python parse_magnet_links.py <link_url>")
        sys.exit(1)

    link_url = sys.argv[1]
    magnet_links = parse_magnet_links(link_url)
    print("Magnet Links:")
    for magnet_link, inner_text in magnet_links:
        print(f"[{inner_text}]({magnet_link})")
