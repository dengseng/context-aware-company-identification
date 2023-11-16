from bs4 import BeautifulSoup
import json
import tldextract

def read_html_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading from file: {e}")
        return None

def extract_information(html_content, website_name_to_avoid):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    related_companies = set()

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')
        domain_parts = tldextract.extract(href)
        extracted_base_domain = f"{domain_parts.domain}.{domain_parts.suffix}"

        if "twitter.com" in extracted_base_domain.lower() or "t.co" in extracted_base_domain.lower():
            company_name, company_domain = "X", "x.com"
        elif extracted_base_domain and extracted_base_domain != ".":
            company_name, company_domain = tldextract.extract(extracted_base_domain).domain, extracted_base_domain
        else:
            continue

        if company_name.lower() != website_name_to_avoid.lower():
            related_companies.add((company_name, company_domain.lower()))

    unique_companies = [{"company_name": name, "company_domain": domain} for name, domain in related_companies]

    # Extract the main topic and exclude the website name
    title = soup.title.text.strip()
    topic = title.split('|')[0].strip()

    result = {"related_companies": unique_companies, "topic": topic}

    return result

# Example usage:
file_path = "article.html"
website_name_to_avoid = "Techcrunch"  # Replace with the specific website name to avoid
html_content = read_html_from_file(file_path)

if html_content:
    extracted_info = extract_information(html_content, website_name_to_avoid)

    if extracted_info:
        # Display the extracted information
        print(json.dumps(extracted_info, indent=2))
    else:
        print("Failed to extract information from the HTML content.")
else:
    print("Failed to read HTML content from the file.")


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