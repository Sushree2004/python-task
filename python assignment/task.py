import sqlite3
import requests
from bs4 import BeautifulSoup

# Step 1: Extract Data
URL = "https://www.tpointtech.com/"
r = requests.get(URL)

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content, 'html5lib')

content = []  # a list to store extracted content

main_content = soup.find('div', attrs={'class': 'mw-parser-output'})
if main_content:
    for section in main_content.find_all(['h2', 'h3', 'p'], recursive=False):
        if section.name == 'h2' or section.name == 'h3':  # Extracting section headings
            content.append({'type': 'heading', 'text': section.text.strip()})
        elif section.name == 'p':  # Extracting paragraphs
            content.append({'type': 'paragraph', 'text': section.text.strip()})

# Step 2: Set up SQLite database
conn = sqlite3.connect('content.db')  # Create (or connect to) a SQLite database
cursor = conn.cursor()

# Step 3: Create Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Content (
    id INTEGER PRIMARY KEY,
    type TEXT,
    text TEXT
)
''')

# Step 4: Insert Data into the Table
for item in content:
    cursor.execute('INSERT INTO Content (type, text) VALUES (?, ?)', (item['type'], item['text']))

# Step 5: Commit Changes and Close the Connection
conn.commit()
conn.close()

print("Data has been successfully inserted into the database.")
