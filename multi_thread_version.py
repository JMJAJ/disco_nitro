import requests
import random
import json
import time
from concurrent.futures import ThreadPoolExecutor

def get_proxies():
    with open('final.json', 'r') as file:
        proxies = json.load(file)
    return proxies

def get_current_proxy(proxies, index):
    return proxies[index]

def make_request(proxy, url, headers, data, proxy_type):
    try:
        proxies = {proxy_type: f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"}
        headers['X-Forwarded-For'] = f"{proxy['ip']}"
        response = requests.post(url, headers=headers, proxies=proxies, json=data)
        
        print("Response Headers:", response.headers, "\n")

        if response.status_code == 200:
            result = response.json()
            with open('output_all.json', 'a') as file:
                json.dump(result, file)
                file.write(',')
                file.write('\n')
                # print(result)
        elif response.status_code == 429:
            print(f"Rate limit exceeded for proxy {proxy['ip']}. Moving to the next proxy.")
        time.sleep(5e-2)
    except Exception as e:
        print(f"Error with proxy {proxy['ip']}: {str(e)}")

url = 'https://api.discord.gx.games/v1/direct-fulfillment'
headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,cs-CZ;q=0.8,cs;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
}

data = {
    'partnerUserId': '549e62dfd46b230162850b3b8d7871862de68040acf137274571ccaf561178b1'
}

delay_range = (3e-2, 7e-2)

proxies_list = get_proxies()

with ThreadPoolExecutor(max_workers=len(proxies_list)) as executor:
    for proxy in proxies_list:
        executor.submit(make_request, proxy, url, headers, data, proxy_type=proxy['protocol'])
        time.sleep(random.uniform(*delay_range))
