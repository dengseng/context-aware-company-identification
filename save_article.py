import requests
from bs4 import BeautifulSoup

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


def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the main content with a space as separator
    main_content = soup.get_text(separator=' ', strip=True)

    return main_content

if html_content:
    article_content = extract_content(html_content)

    if article_content:
        # Display the extracted article content
        print(article_content)
    else:
        print("Failed to extract content from the HTML file.")
else:
    print("Failed to read HTML content from the file.")
