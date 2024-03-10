from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import requests

try:
    tree = ET.parse('database.xml')
    root = tree.getroot()
except FileNotFoundError:
    root = ET.Element("data")
    tree = ET.ElementTree(root)

USERNAME = "user"
PASSWORD = "12345"
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def save_data(username, password, topic, text, timestamp):
    if not authenticate(username, password):
        return "Authentication failed. Invalid username or password."

    for t in root.findall('topic'):
        if t.get('name') == topic:
            note = ET.SubElement(t, 'note')
            note.set('name', f'{topic} {timestamp}')
            ET.SubElement(note, 'text').text = text
            ET.SubElement(note, 'timestamp').text = timestamp
            tree.write('database.xml')
            return f"The topic '{topic}' already exists, new data has been added."

    new_topic = ET.SubElement(root, 'topic', name=topic)
    note = ET.SubElement(new_topic, 'note', name=f'{topic} {timestamp}')
    ET.SubElement(note, 'text').text = text
    ET.SubElement(note, 'timestamp').text = timestamp
    tree.write('database.xml')
    return f"New topic '{topic}' created and note added."


def get_contents(username, password, topic):
    if not authenticate(username, password):
        return "Authentication failed. Invalid username or password."

    for t in root.findall('topic'):
        if t.get('name') == topic:
            return ET.tostring(t, encoding='unicode')
    return "Topic not found."


def query_wikipedia(username, password, search_term, topic):
    if not authenticate(username, password):
        return "Authentication failed. Invalid username or password."

    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{unquote(search_term)}")
    if response.status_code == 200:
        data = response.json()
        wikipedia_url = data['content_urls']['desktop']['page']
        return add_wikipedia_link_to_topic(wikipedia_url, topic)
    else:
        return "Article not found."


def add_wikipedia_link_to_topic(wikipedia_url, topic):
    for t in root.findall('topic'):
        if t.get('name') == topic:
            wikipedia_link_element = t.find('wikipedia_link')
            if wikipedia_link_element is None:
                ET.SubElement(t, 'wikipedia_link').text = wikipedia_url
                tree.write('database.xml')
                return f"Added Wikipedia link to topic '{topic}': {wikipedia_url}"
            else:
                wikipedia_link_element.text = wikipedia_url
                tree.write('database.xml')
                return f"Updated Wikipedia link for topic '{topic}': {wikipedia_url}"
    return "Topic not found."


server = SimpleXMLRPCServer(('localhost', 8000))
print("Listening on port 8000...")
server.register_function(save_data, "save_data")
server.register_function(get_contents, "get_contents")
server.register_function(query_wikipedia, "query_wikipedia")

server.serve_forever()
