import pandas as pd

def load_rules_from_google_sheet():
    sheet_id = "1ncfPld7-2ASDARZycfqREIkOkb-Ss6Jj"
    SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    df = pd.read_csv(SHEET_CSV_URL, dtype=str).fillna('')
    rules = {}
    for _, row in df.iterrows():
        product_id = row['id'].strip()
        rules[product_id] = {}
        if row['price'].strip():
            rules[product_id]['price'] = row['price'].strip()
        if row['price_promo'].strip():
            rules[product_id]['promo_price'] = row['price_promo'].strip()
        if row['stock_quantity'].strip():
            rules[product_id]['stock_quantity'] = row['stock_quantity'].strip()
    return rules
