# Flask Backend (Python Framework - Python Module)

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='template', static_folder='CSS')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data['url']
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Failed to fetch URL: {str(e)}"}), 400
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting title
    title = soup.title.get_text() if soup.title else 'No title found'

    # Extracting the first image
    img_tag = soup.find('img')
    image_url = img_tag['src'] if img_tag else 'No image found'

    # Extracting all textual content from specific tags (excluding script and style)
    excluded_tags = ['script', 'style']
    included_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div']

    def extract_text(elements):
        text_set = set()
        for element in elements:
            if element.name not in excluded_tags:
                text = ' '.join(element.get_text(separator=' ').split())
                text_set.add(text)
        return ' '.join(sorted(text_set, key=lambda x: elements.index(next(e for e in elements if ' '.join(e.get_text(separator=' ').split()) == x))))

    all_elements = []
    for tag in included_tags:
        all_elements.extend(soup.find_all(tag))

    text_content = extract_text(all_elements)

    # Return the extracted data as JSON response
    return jsonify({
        'title': title,
        'image_url': image_url,
        'summary': text_content
    })

if __name__ == '__main__':
    app.run(debug=True)
