import requests
from bs4 import BeautifulSoup
import json


def make_request(url, headers=None, params=None, http_type="GET", data=None):
    try:
        if http_type == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif http_type == "POST":
            response = requests.post(url, headers=headers, data=data)
        else:
            raise Exception("Wrong HTTP type.")

        response.raise_for_status()  # HTTP hatası varsa exception fırlatır
        return response
    except requests.exceptions.RequestException as e:
        print(f"İstek hatası: {e}")
        return None

def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

def extract_data(soup, selectors):
    """
    BeautifulSoup nesnesinden veri çıkarır.

    Args:
        soup (BeautifulSoup): Ayrıştırılmış HTML
        selectors (dict): Veri çıkarma için seçiciler ve eşleştirme bilgileri
            Örnek: {
                'title': {'selector': 'h1.title', 'attribute': None},
                'price': {'selector': 'span.price', 'attribute': None},
                'image': {'selector': 'img.product-image', 'attribute': 'src'},
            }

    Returns:
        dict: Çıkarılan veriler
    """
    result = {}

    for key, config in selectors.items():
        selector = config['selector']
        attribute = config['attribute']

        elements = soup.select(selector)

        if not elements:
            result[key] = None
            continue

        if attribute:
            values = [el.get(attribute) for el in elements if el.has_attr(attribute)]
        else:
            values = [el.get_text(strip=True) for el in elements]

        # Tek bir sonuç mu yoksa liste mi olmalı
        if len(values) == 1:
            result[key] = values[0]
        else:
            result[key] = values

    return result

def scrape_website(url, selectors, headers=None, params=None, http_type="GET", data=None):

    response = make_request(url, headers, params, http_type=http_type, data=data)

    if not response:
        return json.dumps({"error": "İstek başarısız oldu"})

    soup = parse_html(response.text)
    data = extract_data(soup, selectors)

    return json.dumps(data, ensure_ascii=False, indent=2)

