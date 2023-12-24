import requests
from config import api_key, api_secret
from colorama import Fore, init
import os

# Clear screen
os.system('clear' if os.name == 'posix' else 'cls')

# Initialize colorama
init(autoreset=True)

# Color codes
red = Fore.RED
cyan = Fore.CYAN
white = Fore.WHITE
green = Fore.GREEN
magenta = Fore.MAGENTA
yellow = Fore.YELLOW

# Display PABLO logo
def display_logo():
    print(f"""
{red}███████╗███╗   ███╗███████╗    ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ 
{cyan}██╔════╝████╗ ████║██╔════╝    ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
{white}███████╗██╔████╔██║███████╗    ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
{green}╚════██║██║╚██╔╝██║╚════██║    ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
{magenta}███████║██║ ╚═╝ ██║███████║    ███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║
{yellow}╚══════╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""")

# Disable warnings
requests.urllib3.disable_warnings()

def send_sms(from_number, to_number, message):
    url = 'https://rest.nexmo.com/sms/json'
    params = {
        'api_key': api_key,
        'api_secret': api_secret,
        'from': from_number,
        'to': to_number,
        'text': message,
    }

    response = requests.post(url, params=params)
    data = response.json()

    if 'messages' in data:
        print(f"\033[92mMessage sent successfully\033[0m. \033[94mMessage ID:\033[0m {data['messages'][0]['message-id']}")
    else:
        print(f"\033[91mError sending message:\033[0m {data.get('error-text', 'Unknown error')}")

def send_bulk_sms(from_number, recipient_file_path, message_file_path):
    try:
        with open(recipient_file_path, 'r') as file:
            recipients = file.readlines()

        with open(message_file_path, 'r') as file:
            messages = file.readlines()

        for to_number, message in zip(recipients, messages):
            send_sms(from_number, to_number.strip(), message.strip())

        print('\033[92mBulk SMS sent successfully\033[0m.')
    except FileNotFoundError as e:
        print(f'\033[91mError: {e}\033[0m')
    except Exception as e:
        print(f'\033[91mError sending bulk SMS:\033[0m {e}')

def get_user_input():
    from_number = input('\033[93mEnter sender phone number:\033[0m ')
    to_number = input('\033[93mEnter recipient phone number:\033[0m ')
    message_file_path = input('\033[93mEnter the path to the message file:\033[0m ')
    return from_number, to_number, message_file_path

def get_bulk_sms_input():
    from_number = input('\033[93mEnter sender phone number:\033[0m ')
    recipient_file_path = input('\033[93mEnter the path to the recipient phone number list file:\033[0m ')
    message_file_path = input('\033[93mEnter the path to the message file:\033[0m ')
    return from_number, recipient_file_path, message_file_path


def display_menu():
    print("""
\033[1;36;40mMenu:
1. Send SMS to a specified phone number
2. Send bulk SMS using the file path for the list of phone numbers
3. Exit\033[0m
    """)

def main():
    display_logo()

    while True:
        display_menu()
        choice = input('\033[93mEnter your choice (1, 2, 3):\033[0m ')

        if choice == '1':
            from_number, to_number, message_file_path = get_user_input()
            send_sms(from_number, to_number, message_file_path)
        elif choice == '2':
            from_number, recipient_file_path, message_file_path = get_bulk_sms_input()
            send_bulk_sms(from_number, recipient_file_path, message_file_path)
        elif choice == '3':
            print('\033[92mExiting the Nexmo SMS Sender. Goodbye!\033[0m')
            break
        else:
            print('\033[91mInvalid choice. Please enter a valid option.\033[0m')

if __name__ == "__main__":
    main()
