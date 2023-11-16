import requests

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def save_html_to_file(html_content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML content saved to: {file_path}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Example usage
url = input("Enter the URL of the article: ")
html_content = get_html_content(url)

if html_content:
    file_path = 'article.html'  # Adjust the file name and path as needed
    save_html_to_file(html_content, file_path)
else:
    print("Failed to retrieve HTML content from the URL.")
