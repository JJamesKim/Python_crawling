from bs4 import BeautifulSoup
import requests
import re


url = "http://www.edaily.co.kr/news/newspath.asp?newsid=03181606635710600"

response = requests.get(url, verify=False)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

br_list = []


for tag in soup.select('div br'):
    # Extract text from <br> tag and remove anything between < and >
    cleaned_text = re.sub(r'<[^>]*>', '', str(tag.next))
    # Remove escape codes starting with '\'
    cleaned_text = re.sub(r'\\.*', '', cleaned_text)

    # Check if cleaned text (after stripping) is not empty
    if cleaned_text.strip():
        br_list.append(cleaned_text.strip())

    print(br_list)
    print("-" * 30)

# br_list의 개수 출력
print("br_list의 개수:", len(br_list))