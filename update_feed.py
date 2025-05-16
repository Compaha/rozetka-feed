import requests
import xml.etree.ElementTree as ET
from rules_from_sheet import load_rules_from_google_sheet

URL = 'https://spacecoffee.com.ua/rozetka_feed.xml?rozetka_hash_tag=82bd98fae0147bcfa185b059b5e7c1dd&product_ids=&label_ids=1651385&languages=uk%2Cru&group_ids='
OUTPUT_FILE = 'output/feed.xml'

def apply_rules_to_offer(offer, rule):
    for tag in ['price', 'promo_price', 'stock_quantity']:
        if tag in rule:
            elem = offer.find(tag)
            if elem is not None:
                elem.text = str(rule[tag])
            else:
                new_elem = ET.SubElement(offer, tag)
                new_elem.text = str(rule[tag])

def fetch_feed(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def modify_feed(xml_data, rules):
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    for offer in root.findall('.//offer'):
        offer_id = offer.get('id')
        if offer_id in rules:
            apply_rules_to_offer(offer, rules[offer_id])
    tree.write(OUTPUT_FILE, encoding='utf-8', xml_declaration=True)

def main():
    rules = load_rules_from_google_sheet()
    xml_data = fetch_feed(URL)
    modify_feed(xml_data, rules)
    print("Фід оновлено.")

if __name__ == '__main__':
    main()
