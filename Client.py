import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:8000')

def send_data(username, password):
    topic = input("Enter topic: ")
    text = input("Enter text: ")
    timestamp = input("Enter timestamp (MM/DD/YY - HH:MM:SS): ")
    response = server.save_data(username, password, topic, text, timestamp)
    print(response)

def get_data(username, password):
    topic = input("Enter topic to fetch: ")
    response = server.get_contents(username, password, topic)
    print(response)

def query_wikipedia(username, password):
    search_term = input("Enter search term for Wikipedia: ")
    topic = input("Enter the topic to associate with this Wikipedia link: ")
    response = server.query_wikipedia(username, password, search_term, topic)
    print(response)

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    while True:
        print("\nOptions:\n1. Send Data\n2. Get Data\n3. Query Wikipedia\n4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            send_data(username, password)
        elif choice == '2':
            get_data(username, password)
        elif choice == '3':
            query_wikipedia(username, password)
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
