# icv_login.py
import os
import requests
from bs4 import BeautifulSoup

def icv_login():
    # Step 1: Initial GET request
    url = 'https://www.icv-crew.com/forum/index.php?action=login'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'it',
        'Connection': 'keep-alive',
        'Host': 'www.icv-crew.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url, headers=headers)

    get_cookies = response.headers.get('Set-Cookie', '')

    # Split the "Set-Cookie" header into individual cookies
    get_cookie_parts = get_cookies.split(';')

    # Find the cookie with the name "PHPSESSID" and extract its value
    get_phpsessid_match = None
    for part in get_cookie_parts:
        if 'PHPSESSID' in part:
            get_phpsessid_match = part.split('=')[1].strip()
            break

    # print(f'PHPSESSID Match: {get_phpsessid_match}')

    # Print collected cookie headers
    # print(f'GET Response Headers: {response.headers}')
    # print(f'Parsed PHPSESSID: {get_phpsessid_match}')

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract required values from the HTML response
    name_attr_value = soup.find_all('input', type='hidden')[1]['name']
    value_attr_value = soup.find_all('input', type='hidden')[1]['value']

    # Print collected cookie headers
    # print(f'"name" attribute: {name_attr_value}')
    # print(f'"value" attribute: {value_attr_value}')

    # Step 2: Make POST request with authentication data
    url_post = f'https://www.icv-crew.com/forum/index.php?action=login2'
    headers_post = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'it',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'PHPSESSID={get_phpsessid_match}',
        'Host': 'www.icv-crew.com',
        'Origin': 'https://www.icv-crew.com',
        'Referer': 'https://www.icv-crew.com/forum/index.php?action=login',
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

    # Use environment variables for username and password
    data_post = {
        'user': os.getenv('ICV_USERNAME'),
        'passwrd': os.getenv('ICV_PASSWORD'),
        'cookieneverexp': 'on',
        name_attr_value: value_attr_value,
        'hash_passwrd': '',  # Add the actual value for hash_passwrd
    }

    # Include cookies in the POST request
    cookies = {'PHPSESSID': get_phpsessid_match}
    response_post = requests.post(url_post, headers=headers_post, data=data_post, cookies=cookies, allow_redirects=False)

    # Debugging lines
    # print(f'\nPOST Request URL: {response_post.request.url}')
    # print(f'POST Request Headers: {response_post.request.headers}')
    # print(f'POST Request Body: {response_post.request.body}')

    # Debugging line to check if cookies are being sent in the POST request
    # print(f'POST Request Cookies: {response_post.request._cookies}')

    # Debugging lines to check the response from the POST request
    # print(f'\nPOST Response Status Code: {response_post.status_code}')
    # print(f'POST Response Headers: {response_post.headers}')
    # print(f'POST Response Text: {response_post.text}')



    # Extract both "PHPSESSID" and "SMFCookie68" cookies from the response headers
    post_cookies = response_post.headers.get('Set-Cookie', '')

    # Debugging line to check the raw Set-Cookie header in the response
    # print(f'\nRaw Set-Cookie Header in POST Response: {post_cookies}')

    post_phpsessid_match = None
    post_smfcookie68_match = None

    # Split the "Set-Cookie" header into individual cookies
    post_cookie_parts = post_cookies.split(';')

    for cookie in post_cookie_parts:
        if 'PHPSESSID' in cookie:
            post_phpsessid_match = cookie.split('=')[1].strip()
        elif 'SMFCookie68' in cookie:
            post_smfcookie68_match = cookie.split('=')[1].strip()

    # print(f'POST PHPSESSID: {post_phpsessid_match}')
    # print(f'POST SMFCookie68: {post_smfcookie68_match}')

    # Store cookies in a file
    with open('./data/session_cookie.txt', 'w') as file:
        file.write(f'PHPSESSID={post_phpsessid_match}\n')
        if post_smfcookie68_match:
            file.write(f'SMFCookie68={post_smfcookie68_match}\n')

    # print('Login successful. Session cookies saved to ./data/session_cookie.txt.')



    # Check if there's a redirect
    if response_post.status_code == 302:
        redirect_url = response_post.headers.get('Location')
        # print(f'Redirect URL: {redirect_url}')

        # Make a new GET request to the redirect URL to capture the final response
        response_post = requests.get(redirect_url, headers=headers_post, cookies=cookies)
    
    pass
    
if __name__ == "__main__":
    icv_login()