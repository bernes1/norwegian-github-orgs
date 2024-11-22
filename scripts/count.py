import json 

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data = load_json_file('merged_github_orgs.json')

count = len(data)

print(f"Total number of GitHub organizations: {count}")