from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET
from rules_from_sheet import load_rules_from_google_sheet

app = Flask(__name__)

PROM_URL = 'https://spacecoffee.com.ua/rozetka_feed.xml?rozetka_hash_tag=82bd98fae0147bcfa185b059b5e7c1dd&product_ids=&label_ids=1651385&languages=uk%2Cru&group_ids='

def apply_rules_to_offer(offer, rule):
    for tag in ['price', 'promo_price', 'stock_quantity']:
        if tag in rule:
            elem = offer.find(tag)
            if elem is not None:
                elem.text = str(rule[tag])
            else:
                new_elem = ET.SubElement(offer, tag)
                new_elem.text = str(rule[tag])

def generate_modified_feed():
    response = requests.get(PROM_URL)
    response.raise_for_status()
    xml_data = response.content

    rules = load_rules_from_google_sheet()
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    for offer in root.findall('.//offer'):
        offer_id = offer.get('id')
        if offer_id in rules:
            apply_rules_to_offer(offer, rules[offer_id])

    xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    return xml_bytes

@app.route('/feed.xml')
def feed():
    xml_content = generate_modified_feed()
    return Response(xml_content, mimetype='application/xml')

@app.route('/')
def home():
    return '<h2>Rozetka XML feed service is running ✅</h2><p>Access feed at <a href="/feed.xml">/feed.xml</a></p>'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
