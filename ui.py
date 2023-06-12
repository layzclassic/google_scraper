import concurrent.futures
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import socket
import webbrowser
import tkinter as tk
from tkinter import filedialog


def scrape_web(query, num_results):
    query = query.replace(' ', '+')
    url = f"https://google.com/search?q={query}&num={num_results}"
    print("Scraping URL:", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        print('Soup completed')
    else:
        print('Error: Failed to retrieve search results')
        return []

    results = []
    urls_list = []
    for g in soup.find_all('div', class_='yuRUbf'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            urls_list.append(link)
            title = g.find('h3').text
            item = {
                "title": title,
                "url": link
            }
            results.append(item)

    for row in results:
        print(row)
    return results


def scrape_url(url):
    try:
        response = requests.get(url)
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.(?:com|au)", response.text, re.I))
        response.close()  # Close the response to release the connection

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string

        # DNS lookup to get the name associated with the email
        email_data = []
        for email in new_emails:
            name = socket.getfqdn(email).split('.')[0]
            email_data.append({'email': email, 'name': name})

        return {'title': title, 'url': url, 'emails': email_data}

    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return {'title': '', 'url': url, 'emails': []}


def scrape(websites, max_workers):
    print("Scraping URLs for emails...")
    start_time = time.time()
    total_urls = len(websites)
    processed_urls = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(scrape_url, websites)

    emails = set()
    for result in results:
        emails.update(result['emails'])
        processed_urls += 1

        elapsed_time = time.time() - start_time
        avg_time_per_url = elapsed_time / processed_urls if processed_urls > 0 else 0
        remaining_urls = total_urls - processed_urls
        remaining_time = remaining_urls * avg_time_per_url

        print(f"Processed {processed_urls}/{total_urls} URLs. Estimated remaining time: {remaining_time:.2f} seconds")

    return emails


def save(emails, base_name, save_location):
    data = []
    for email in emails:
        data.append({
            'title': email['title'],
            'url': email['url'],
            'email': email['email'],
            'name': email['name']
        })

    header = ['title', 'url', 'email', 'name']
    df = pd.DataFrame(data)
    file_name = f"{base_name}.csv"
    file_path = os.path.join(save_location, file_name)
    df.to_csv(file_path, columns=header, index=False)
    print("Emails saved to:", file_path)


def main(query, num_results, base_name, save_location, max_workers):
    print("Starting web scraping...")
    websites = [item['url'] for item in scrape_web(query, num_results)]
    emails = scrape(websites, max_workers)
    save(emails, base_name, save_location)
    print("Web scraping completed.")


def open_save_location(save_location):
    webbrowser.open(save_location)


def start_scraping():
    query = query_entry.get()
    num_results = int(num_results_entry.get())
    base_name = base_name_entry.get()
    save_location = save_location_entry.get()
    max_workers = int(max_workers_entry.get())

    main(query, num_results, base_name, save_location, max_workers)
    open_save_location(save_location)


# Create the main window
window = tk.Tk()
window.title("Web Scraping Tool")

# Query input
query_label = tk.Label(window, text="Query:")
query_label.pack()
query_entry = tk.Entry(window, width=50)
query_entry.pack()

# Number of results input
num_results_label = tk.Label(window, text="Number of results:")
num_results_label.pack()
num_results_entry = tk.Entry(window, width=50)
num_results_entry.pack()

# Base name input
base_name_label = tk.Label(window, text="Base name:")
base_name_label.pack()
base_name_entry = tk.Entry(window, width=50)
base_name_entry.pack()

# Save location input
save_location_label = tk.Label(window, text="Save location:")
save_location_label.pack()
save_location_entry = tk.Entry(window, width=50)
save_location_entry.pack()

# Max workers input
max_workers_label = tk.Label(window, text="Max workers:")
max_workers_label.pack()
max_workers_entry = tk.Entry(window, width=50)
max_workers_entry.pack()

# Start scraping button
scrape_button = tk.Button(window, text="Start Scraping", command=start_scraping)
scrape_button.pack()

# Save location button
save_location_button = tk.Button(window, text="Open Save Location", command=lambda: open_save_location(save_location_entry.get()))
save_location_button.pack()

# Run the main event loop
window.mainloop()
