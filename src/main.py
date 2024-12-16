import sqlite3
import json

con = sqlite3.connect("test-orgs.db")
cur = con.cursor()

def setup():
  cur.execute("""
  CREATE TABLE IF NOT EXISTS category (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(255) NOT NULL UNIQUE
  );
  """)
  
  
  cur.execute("""CREATE TABLE IF NOT EXISTS github_org (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(255) NOT NULL,
      url VARCHAR(255) NOT NULL,
      username VARCHAR(255) NOT NULL,
      user_id INTEGER NOT NULL,
      category_id INTEGER NOT NULL,
      FOREIGN KEY (category_id) REFERENCES category(id)
  );
  """)
  
  cur.execute("INSERT INTO category (name) VALUES ('private-sector')")
  cur.execute("INSERT INTO category (name) VALUES ('public-sector')")
  cur.execute("INSERT INTO category (name) VALUES ('other')")
    
  con.commit()
  con.close()

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def find_orgs(search_term, category_id):
    data = load_json_file("merged_github_orgs.json")
    count = 0
    for org in data:
       name = org["name"]
       if search_term in name.lower():
          count += 1
          #print(f"{name} {count}")
          pretty_output = json.dumps(org, indent=4)
          cur.execute("INSERT INTO github_org (name, url, username, user_id, category_id) VALUES (?, ?, ?, ?, ?)", (org["name"], org["html_url"], org["login"], org["id"], category_id))
          print(pretty_output)
         
    con.commit()
    con.close()
    print(count)
   
def feed_json_to_db(): 
    find_orgs("-as", 1)

#setup()
feed_json_to_db()
#TODO: complete this 

