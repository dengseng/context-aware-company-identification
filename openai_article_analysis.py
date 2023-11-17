import os
from openai import OpenAI
import json
from bs4 import BeautifulSoup
import tldextract

# Create an OpenAI client using the API key from the environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove title and navigation tools
    for element in soup(["title", "nav", "header"]):
        element.extract()

    # Extract the main content with a space as separator
    main_content = soup.get_text(separator=' ', strip=True)

    return main_content


def generate_gpt3_prompt(extracted_info, article_content):
    topic = extracted_info["topic"]
    related_companies = [company["company_name"] for company in extracted_info["related_companies"]]
    article_content = article_content[:3000]  # Limit the content to 2000 tokens for GPT-3 prompt

    # Construct the prompt with extracted content
    prompt = f"Based on the information extracted:\n\nTopic: {topic}\nRelated Companies: {', '.join(related_companies)}\n\nArticle Content: {article_content}\n\nIdentify and list companies directly related to the main theme of the article. Include companies that play a significant role in the topic or have reported on relevant activities. Provide specific details about each mentioned company's role or connection to the central theme discussed in the article."

    return prompt

def make_gpt3_api_call(client, prompt):
    return client.completions.create(
        model='text-davinci-003',  # Adjust the model based on your preference
        prompt=prompt,
        max_tokens=200  # Adjust max_tokens based on the desired length of the response
    )

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

# Main
file_path = "article.html"
website_name_to_avoid = "Techcrunch"
html_content = read_html_from_file(file_path)

if html_content:
    extracted_info = extract_information(html_content, website_name_to_avoid)

    if extracted_info:
        # Extract content from HTML
        article_content = extract_content(html_content)

        # Display the extracted information
        print(json.dumps(extracted_info, indent=2))

        # Generate the GPT-3 prompt
        gpt3_prompt = generate_gpt3_prompt(extracted_info, article_content)
        
        # API call will likely fail due to insufficient quota
        # Used direct prompt on free to use GPT3.5
        print(gpt3_prompt)

        # Make an API call to GPT-3
        try:
            completion = make_gpt3_api_call(client, gpt3_prompt)

            # Extract the generated text from the GPT-3 response
            generated_text = completion.choices[0].text

            # Print the generated text
            print(generated_text)
        except Exception as e:
            print(f"Error making API call to GPT-3: {e}")
    else:
        print("Failed to extract information from the HTML content.")
else:
    print("Failed to read HTML content from the file.")
