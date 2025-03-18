from flask import Flask, render_template, request, jsonify, send_file
from JustDial import JustDialScraper
import os
from datetime import datetime
import threading

app = Flask(__name__)
scraper = JustDialScraper()

# Store scraping status
scraping_status = {
    'is_running': False,
    'total_pages': 0,
    'current_page': 0,
    'results': [],
    'latest_file': None,
    'error': None
}

# Get absolute path for data directory
def get_data_dir():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'Just Data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def scraping_callback(progress_data):
    """Callback function to update scraping status"""
    scraping_status['current_page'] = progress_data['current_page']
    scraping_status['results'].extend(progress_data['page_data'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    data = request.json
    base_url = data.get('url')
    start_page = int(data.get('start_page', 1))
    end_page = int(data.get('end_page', 20))

    if not scraping_status['is_running']:
        scraping_status['is_running'] = True
        scraping_status['total_pages'] = end_page - start_page + 1
        scraping_status['current_page'] = 0
        scraping_status['error'] = None

        thread = threading.Thread(
            target=run_scraping,
            args=(base_url, start_page, end_page)
        )
        thread.start()

        return jsonify({'status': 'started'})
    return jsonify({'status': 'already_running'})

def run_scraping(base_url, start_page, end_page):
    try:
        scraping_status['results'] = []
        scraping_status['error'] = None
        
        # Run the scraper with callback
        file_path = scraper.scrape_multiple_pages(
            base_url=base_url,
            start_page=start_page,
            end_page=end_page,
            callback=scraping_callback
        )
        
        if file_path:
            scraping_status['latest_file'] = os.path.basename(file_path)
            
    except Exception as e:
        scraping_status['error'] = str(e)
        print(f"Error during scraping: {e}")
    finally:
        scraping_status['is_running'] = False

@app.route('/status')
def get_status():
    return jsonify({
        'is_running': scraping_status['is_running'],
        'progress': scraping_status['current_page'],
        'total_pages': scraping_status['total_pages'],
        'results_count': len(scraping_status['results']),
        'latest_file': scraping_status['latest_file'],
        'error': scraping_status['error']
    })

@app.route('/download_latest')
def download_latest():
    if scraping_status['latest_file']:
        try:
            data_dir = get_data_dir()
            file_path = os.path.join(data_dir, scraping_status['latest_file'])
            
            if os.path.exists(file_path):
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=scraping_status['latest_file']
                )
            else:
                return jsonify({'error': 'File not found on server'}), 404
        except Exception as e:
            return jsonify({'error': f'Error downloading file: {str(e)}'}), 500
    return jsonify({'error': 'No file available'}), 404

if __name__ == '__main__':
    # Ensure data directory exists on startup
    get_data_dir()
    app.run(debug=True, port=5000) 