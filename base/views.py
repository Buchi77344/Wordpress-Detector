from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.contrib import messages

def detect(request):
    if 'url' in request.GET:
        url = request.GET['url']
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Check for WordPress specific patterns
                wordpress_detected = False
                
                # Check for meta generator tag
                if soup.find('meta', {'name': 'generator', 'content': 'WordPress'}):
                    wordpress_detected = True

                # Check for WordPress specific classes
                elif soup.find(class_='wp-block') or soup.find(class_='wp-post-image'):
                    wordpress_detected = True

                # Check for common WordPress folder and file paths
                elif '/wp-content/' in html_content or '/wp-includes/' in html_content:
                    wordpress_detected = True

                # Add more detection rules as needed

                if wordpress_detected:
                    messages.success(request, 'WordPress detected!')
                else:
                    messages.warning(request, 'WordPress not detected.')
            else:
                messages.error(request, f'Failed to fetch URL: {response.status_code}')
        except Exception as e:
            messages.error(request, f'An error occurred: you are offline')
    else:
        messages.error(request, 'Missing URL parameter')

    return render(request, 'detect.html', {'messages': messages.get_messages(request)})
