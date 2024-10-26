import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() 

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def write_json_file(data, file_name):  
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Full GitHub URLs have been saved to {file_name}")
    
def write_json_file_merged(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Merged data has been saved to {file_name}")
    
def merge_json_files(file_paths):
    merged_data = []
    seen = set()
    
    for file_path in file_paths:
        data = load_json_file(file_path)
        for item in data:
            identifier = item['login']  # or 'id'
            if identifier not in seen:
                seen.add(identifier)
                merged_data.append(item)
    
    return merged_data

def search_github_orgs(query, token, year):
    url = 'https://api.github.com/search/users'
    headers = {'Authorization': f'token {token}'}
    page = 1
    has_more_pages = True
    github_orgs = []

    while has_more_pages:
        params = {'q': f'type:org {query} repos:>1 created:{year}-01-01..{year}-12-31', 'per_page': 100, 'page': page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            orgs = response.json()['items']
            if not orgs:
                break  # Exit if no organizations are returned
            for org in orgs:
                org_name = org['login']
                org_details_response = requests.get(f'https://api.github.com/orgs/{org_name}', headers=headers)
                if org_details_response.status_code == 200:
                    org_details = org_details_response.json()
                    org['name'] = org_details.get('login')
                    org['avatar_url'] = org_details.get('avatar_url')
                else:
                    print(f"Failed to fetch details for {org_name}. Status Code: {org_details_response.status_code}. Response: {org_details_response.text}")
                number = orgs.index(org) + 1 + ((page - 1) * 100)
                print(f"{number}. Org login: {org['login']}, URL: {org['html_url']}, Name: {org.get('name')}")
                github_orgs.append(org)
                
            if len(orgs) < 100:
                has_more_pages = False  # Last page   
            else:
                page += 1  # Prepare for the next page 
                print(page)   
            write_json_file(github_orgs, f'github_orgs_{year}.json') 
        else:
            print(f"Failed to search GitHub: {response.status_code}, Response: {response.text}")
            break

# List of JSON files to merge
json_files = [
    'github_orgs_2010.json',
    'github_orgs_2011.json',
    'github_orgs_2012.json',
    'github_orgs_2010.json',
    'github_orgs_2011.json',
    'github_orgs_2012.json',
    'github_orgs_2013.json',
    'github_orgs_2014.json',
    'github_orgs_2015.json',
    'github_orgs_2016.json',
    'github_orgs_2017.json',
    'github_orgs_2018.json',
    'github_orgs_2019.json',
    'github_orgs_2020.json',
    'github_orgs_2021.json',
    'github_orgs_2022.json',
    'github_orgs_2023.json',
]

# Your GitHub personal access token
token = os.getenv('GHTOKEN')
# Example search query
query = 'location:"Norway"'

# Iterate over the range of years and fetch repositories for each year
for year in range(2010, 2024):
    print(f"Fetching data for year {year}...")
    print(f"Searching for GitHub organizations with query: {query}")
    #search_github_orgs(query, token, year)
    
print("Data fetching completed!")

# Merge the JSON files and remove duplicates
merged_data = merge_json_files(json_files)

# Write the merged data to a new JSON file
write_json_file(merged_data, 'merged_github_orgs.json')

print("Done!")