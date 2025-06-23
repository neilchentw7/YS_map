import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

CSV_PATH = 'site_locations.csv'
_SHEET_NAME = 'locations'
_sheet = None


def _init_sheet():
    """Initialize and cache the Google Sheet instance."""
    global _sheet
    if _sheet is not None:
        return _sheet

    creds_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')

    if not creds_json or not spreadsheet_id:
        try:
            import streamlit as st
            creds_json = creds_json or st.secrets.get('gcp_service_account')  # type: ignore
            spreadsheet_id = spreadsheet_id or st.secrets.get('spreadsheet_id')  # type: ignore
        except Exception:
            pass

    if not creds_json or not spreadsheet_id:
        raise RuntimeError(
            'Google Sheets credentials not configured. Set GOOGLE_SERVICE_ACCOUNT_JSON '
            'and SPREADSHEET_ID or configure them in Streamlit secrets.'
        )

    creds_info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    try:
        _sheet = spreadsheet.worksheet(_SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        _sheet = spreadsheet.sheet1
        _sheet.update_title(_SHEET_NAME)
    return _sheet




def init_db():
    sheet = _init_sheet()
    if len(sheet.get_all_values()) == 0 and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype={'聯絡電話': str})
        rows = [df.columns.tolist()] + df.values.tolist()
        sheet.append_rows(rows)


def get_all_locations():
    sheet = _init_sheet()
    rows = sheet.get_all_values()
    if not rows:
        return pd.DataFrame(columns=['id', '工地名稱', '地址', 'GoogleMap網址', '工地主任', '聯絡電話'])
    header, *data = rows
    df = pd.DataFrame(data, columns=header)
    df.insert(0, 'id', range(2, len(data) + 2))
    return df


def add_location(name, address, url, supervisor, phone):
    sheet = _init_sheet()
    sheet.append_row([name, address, url, supervisor, phone])


def delete_location(row_id):
    sheet = _init_sheet()
    sheet.delete_rows(int(row_id))
