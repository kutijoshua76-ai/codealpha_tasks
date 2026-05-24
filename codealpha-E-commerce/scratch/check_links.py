import urllib.request
import re

try:
    with urllib.request.urlopen('http://localhost:8000/') as response:
        html = response.read().decode('utf-8')
        # Look for the footer area specifically
        footer_links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', html)
        for href, text in footer_links:
            text_clean = text.strip()
            if any(k in text_clean for k in ['About Us', 'FAQ', 'Privacy Policy']):
                print(f"Text: '{text_clean}', Href: '{href}'")
except Exception as e:
    print(f"Error: {e}")
