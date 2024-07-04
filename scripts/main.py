import requests
import json
import dotenv
import os

dotenv.load_dotenv()

def wrtie_json_file(data, file_name):  
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Full GitHub URLs have been saved to {file_name}")

def search_github_orgs(query, token):
    url = 'https://api.github.com/search/users'
    headers = {'Authorization': f'token {token}'}
    page = 1
    has_more_pages = True
    github_orgs = []

    while has_more_pages:
        params = {'q': f'type:org {query} repo:>1', 'per_page': 100, 'page': page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            orgs = response.json()['items']
            if not orgs:
                break  # Exit if no organizations are returned
            for org in orgs:
                number = orgs.index(org) + 1 + ((page - 1) * 100)
                print(f"{number}. Org login: {org['login']}, URL: {org['html_url']}")
                github_orgs.append(org)
                
            if len(orgs) < 100:
                has_more_pages = False  # Last page   
            else:
                page += 1  # Prepare for the next page 
                print(page)   
            wrtie_json_file(github_orgs, 'github_orgs.json') 
        else:
            print(f"Failed to search GitHub: {response.status_code}, Response: {response.text}")
            break

# Your GitHub personal access token
token = os.getenv('GHTOKEN')
# Example search query
query = 'location:"Norway"'

search_github_orgs(query, token)
