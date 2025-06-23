import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

CSV_PATH = 'site_locations.csv'
COLLECTION_NAME = 'locations'

# Initialize Firebase app using a service account key.
# The path can be provided via the FIREBASE_CREDENTIALS environment variable
# or defaults to 'firebase_credentials.json'.
cred_path = os.environ.get('FIREBASE_CREDENTIALS', 'firebase_credentials.json')
if not firebase_admin._apps:
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        raise FileNotFoundError(
            f"Firebase credential file not found: {cred_path}. "
            "Set FIREBASE_CREDENTIALS environment variable to the correct path."
        )

db = firestore.client()

def init_db():
    """Populate Firestore with initial data from CSV if empty."""
    docs = list(db.collection(COLLECTION_NAME).limit(1).stream())
    if not docs and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype={'聯絡電話': str})
        for _, row in df.iterrows():
            db.collection(COLLECTION_NAME).add({
                'name': row['工地名稱'],
                'address': row['地址'],
                'url': row['GoogleMap網址'],
                'supervisor': row['工地主任'],
                'phone': row['聯絡電話'],
            })

def get_all_locations():
    """Return all locations as a DataFrame."""
    docs = db.collection(COLLECTION_NAME).stream()
    records = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        records.append(data)
    df = pd.DataFrame(records)
    if df.empty:
        df = pd.DataFrame(columns=['id', 'name', 'address', 'url', 'supervisor', 'phone'])
    df.rename(columns={
        'name': '工地名稱',
        'address': '地址',
        'url': 'GoogleMap網址',
        'supervisor': '工地主任',
        'phone': '聯絡電話',
    }, inplace=True)
    return df

def add_location(name, address, url, supervisor, phone):
    """Add a new location to Firestore."""
    db.collection(COLLECTION_NAME).add({
        'name': name,
        'address': address,
        'url': url,
        'supervisor': supervisor,
        'phone': phone,
    })

def delete_location(doc_id):
    """Delete a location from Firestore by document id."""
    db.collection(COLLECTION_NAME).document(doc_id).delete()

