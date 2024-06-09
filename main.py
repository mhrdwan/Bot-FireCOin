import requests
import os
import json
import time
from colorama import init, Fore, Style


# Inisialisasi colorama
init(autoreset=True)

base_url = 'https://app2.firecoin.app/api/'

def get_token_from_file(file_path):
    try:
        abs_path = os.path.abspath(file_path)  
        with open(abs_path, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()] 
            return tokens
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {file_path}")
        return None
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return None

def get_firecoin_state(token):
    endpoint = 'loadState'
    url = f"{base_url}{endpoint}"

    headers = {
        'Authorization': token
    }

    try:
        response = requests.post(url, json={}, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
     
        data = response.json()
        total_coin = data.get('clicks', 0)
        total_claim = data.get('wood', {}).get('count', 0)
        
        # print(f"{Fore.CYAN}Response Data: {json.dumps(data, indent=4)}")
        # print(f"{Fore.YELLOW}Total Coin: {total_coin}")
        # print(f"{Fore.YELLOW}Total Claim: {total_claim}")
        
        return {'data': data, 'total_coin': total_coin, 'total_claim': total_claim}

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}HTTP request failed: {e}")
        return None
    except ValueError:
        print(f"{Fore.RED}Failed to decode JSON response")
        return None

def klikKoin(token, total_coin, total_claim):
    totalan = total_claim + total_coin
    endpoint = 'click'
    url = f"{base_url}{endpoint}"
    
    print(f"{Fore.MAGENTA}Total Claim + Total Coin: {totalan}")
    
    payload = {"clicks": totalan}  
    headers = {
        'Authorization': token
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"{Fore.GREEN} {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}HTTP request failed: {e}")

# Usage example
token = get_token_from_file('token.txt')
# print(token)

print(f"{Fore.RED}===============+++===============")

# Membaca token dari file token.txt
tokens = get_token_from_file('token.txt')
if tokens:
    # Mencetak token yang telah dibaca
    print(tokens)
    
    for token in tokens:
        print(token)
        
    print(f"{Fore.RED}===============+++===============")
    
    # Memulai perulangan utama
    while True:
        for token in tokens:  # Loop melalui setiap token
            dataAawal = get_firecoin_state(token)
            if dataAawal is not None:
                klikKoin(token, dataAawal['total_coin'], dataAawal['total_claim'])
                print(f"{Fore.YELLOW}Menunggu 10 detik...")
                print(f"{Fore.RED}===============+++===============")
                time.sleep(10)  # Delay 10 detik
else:
    print(f"{Fore.RED}Token tidak tersedia.")