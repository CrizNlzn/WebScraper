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

    # Extracting all textual content (excluding script and style tags)
    excluded_tags = ['script', 'style']
    text_content = ' '.join([p.get_text(separator='\n') for p in soup.find_all('p') if p not in excluded_tags])
    text_content += ' '.join([div.get_text(separator='\n') for div in soup.find_all('div') if div.get('class') and 'content' in div.get('class') and div not in excluded_tags])
    
    # Return the extracted data as JSON response
    return jsonify({
        'title': title,
        'image_url': image_url,
        'summary': text_content
    })

if __name__ == '__main__':
    app.run(debug=True)
