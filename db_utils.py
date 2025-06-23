import os
import base64
import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

CSV_PATH = 'site_locations.csv'
_collection = 'locations'
_db = None


def _init_firestore():
    global _db
    if _db is not None:
        return _db
    cred = None
    cred_path = os.environ.get('FIREBASE_CREDENTIALS')
    cred_b64 = os.environ.get('FIREBASE_CREDENTIALS_B64')
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
    elif cred_b64:
        data = base64.b64decode(cred_b64)
        cred = credentials.Certificate(json.loads(data))
    else:
        # Attempt to load from Streamlit secrets
        try:
            import streamlit as st
            if 'firebase_credentials_b64' in st.secrets:
                data = base64.b64decode(st.secrets['firebase_credentials_b64'])
                cred = credentials.Certificate(json.loads(data))
            elif 'firebase_credentials' in st.secrets:
                cred = credentials.Certificate(dict(st.secrets['firebase_credentials']))
        except Exception:
            pass
    if not cred:
        raise RuntimeError(
            'Firebase credentials not configured. Set FIREBASE_CREDENTIALS or '
            'FIREBASE_CREDENTIALS_B64, or configure firebase_credentials_b64 in '
            'Streamlit secrets.'
        )
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    _db = firestore.client()
    return _db


def init_db():
    db = _init_firestore()
    # populate from CSV if collection empty
    docs = list(db.collection(_collection).limit(1).stream())
    if not docs and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype={'聯絡電話': str})
        for _, row in df.iterrows():
            db.collection(_collection).add({
                'name': row['工地名稱'],
                'address': row['地址'],
                'url': row['GoogleMap網址'],
                'supervisor': row['工地主任'],
                'phone': row['聯絡電話'],
            })


def get_all_locations():
    db = _init_firestore()
    docs = db.collection(_collection).stream()
    rows = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        rows.append(data)
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=['id', '工地名稱', '地址', 'GoogleMap網址', '工地主任', '聯絡電話'])
    df.rename(columns={
        'name': '工地名稱',
        'address': '地址',
        'url': 'GoogleMap網址',
        'supervisor': '工地主任',
        'phone': '聯絡電話',
    }, inplace=True)
    return df


def add_location(name, address, url, supervisor, phone):
    db = _init_firestore()
    db.collection(_collection).add({
        'name': name,
        'address': address,
        'url': url,
        'supervisor': supervisor,
        'phone': phone,
    })


def delete_location(row_id):
    db = _init_firestore()
    db.collection(_collection).document(row_id).delete()
