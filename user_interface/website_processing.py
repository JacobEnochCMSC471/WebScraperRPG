from bs4 import BeautifulSoup
import os
import requests
import json
import datetime
import pandas as pd


def read_file(filepath: str):
    modified_file_contents = []

    if os.path.isfile(filepath):
        file = open(filepath)

        for line in file:
            modified_file_contents.append(line.strip())

        return modified_file_contents

    else:
        print("File not found! Make sure filepath is correct.")
        return modified_file_contents


def keyword_search(keywords: list, urls: list):
    list_of_hits = {}

    for url in urls:

        if url not in list_of_hits.keys():
            list_of_hits[url] = []

        # Fetch the web page
        response = requests.get(url)

        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()

            # Search for keywords
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    list_of_hits[url].append(keyword)
        else:
            print(f"Failed to fetch {url}")

    return list_of_hits


def scrape_sites(user_provided_keywords: str, user_provided_sites: str, output_file_name: str):
    procurement_sites_no_login = read_file(user_provided_sites)
    keywords = read_file(user_provided_keywords)

    print()

    if not procurement_sites_no_login:
        print("Filepath for procurement sites (no login) list is incorrect. Check filepath and try again!")
        return 1

    if not keywords:
        print("Filepath for keywords list is incorrect. Check filepath and try again!")
        return 1

    list_of_hits = keyword_search(keywords=keywords, urls=procurement_sites_no_login)

    dict_with_keywords = {k: v for k, v in list_of_hits.items() if v}

    json_file_name = "keyword_hits_" + str(datetime.date.today()) + ".json"

    with open(json_file_name, "w") as outfile:
        json.dump(dict_with_keywords, outfile)

    outfile.close()

    # Read JSON data from file
    with open(json_file_name, "r") as file:
        json_data = json.load(file)

    # Determine the maximum length of the keyword lists
    max_len = max(len(keywords) for keywords in json_data.values())

    # Pad the lists with None to make them all the same length
    for url, keywords in json_data.items():
        json_data[url] = keywords + [None] * (max_len - len(keywords))

    # Create a DataFrame
    df = pd.DataFrame(json_data).transpose()

    # Reset index to make the URLs a column instead of index
    df.reset_index(inplace=True)
    df.columns = ['URL'] + list(range(len(df.columns) - 1))  # Rename columns

    # Write DataFrame to Excel
    with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print("Excel file has been created successfully.")

    return 0
