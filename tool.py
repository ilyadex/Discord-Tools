import requests
import time
import keyboard  # Для отслеживания нажатий клавиш
import os
from colorama import Fore, Style, init  # Для цветного текста в консоли

os.system("title Discord Tools")

init(autoreset=True)  # Автоматический сброс цвета после каждой строки

def gradient_text(text):
    colors = [Fore.BLUE, Fore.CYAN]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result + Style.RESET_ALL

BANNER = gradient_text("""
      ::::::::: ::::::::::: ::::::::     ::::::::::: ::::::::   ::::::::  :::        ::::::::
     :+:    :+:    :+:    :+:    :+:        :+:    :+:    :+: :+:    :+: :+:       :+:    :+:
    +:+    +:+    +:+    +:+               +:+    +:+    +:+ +:+    +:+ +:+       +:+        
   +#+    +:+    +#+    +#++:++#++        +#+    +#+    +:+ +#+    +:+ +#+       +#++:++#++  
  +#+    +#+    +#+           +#+        +#+    +#+    +#+ +#+    +#+ +#+              +#+   
 #+#    #+#    #+#    #+#    #+#        #+#    #+#    #+# #+#    #+# #+#       #+#    #+#    
######### ########### ########         ###     ########   ########  ########## ########      
""")
print("made by chatGPT and i1yadex")

def spam_webhook():
    webhook_url = input("Url webhook: ")
    message = input("message for spam: ")
    delay = int(input("Delay (ms): ")) / 1000  # В секундах

    print(f"{Fore.GREEN}esc for stop.{Style.RESET_ALL}")

    while True:
        if keyboard.is_pressed("esc"):
            print(f"{Fore.YELLOW}stopped...{Style.RESET_ALL}")
            break

        response = requests.post(webhook_url, json={"content": message})

        if response.status_code == 204:
            print(f"{Fore.CYAN}Send!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error send: {response.status_code}, {response.text}{Style.RESET_ALL}")

        time.sleep(delay)

def delete_webhook():
    webhook_url = input("Url webhook: ")
    confirm = input(f"{Fore.YELLOW}u sure want del? (y/n): {Style.RESET_ALL}").strip().lower()

    if confirm == "y":
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print(f"{Fore.GREEN}deleted!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error delete webhook: {response.status_code}, {response.text}{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}Stopped.{Style.RESET_ALL}")

def main():
    print(BANNER)
    print("select:")
    print("[1] - Spam webhook")
    print("[2] - Del webhook")
    
    choice = input("Write what u want: ").strip()

    if choice == "1":
        spam_webhook()
    elif choice == "2":
        delete_webhook()
    else:
        print(f"{Fore.RED}wrong number try other!.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
