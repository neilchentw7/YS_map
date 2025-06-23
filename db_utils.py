import os
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

CSV_PATH = "site_locations.csv"
_SHEET_NAME = "locations"
# Default sheet URL for read-only demo when no environment variable or secret is provided
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1VV2AXV7-ZudWApvRiuKW8gcehXOM1CaPXGyHyFvDPQE/edit?gid=0"
_conn = None
_sheet_url = None


def _writing_enabled() -> bool:
    """Return True if writing to the sheet is allowed."""
    return _sheet_url is not None and _sheet_url != DEFAULT_SHEET_URL


def _init_connection():
    """Initialize the Google Sheets connection."""
    global _conn, _sheet_url
    if _conn is not None:
        return _conn

    _sheet_url = os.environ.get("GSHEET_URL")
    if not _sheet_url:
        _sheet_url = st.secrets.get("public_gsheet_url", None)  # type: ignore

    # Fall back to the default sample sheet
    if not _sheet_url:
        _sheet_url = DEFAULT_SHEET_URL
        st.warning(
            "⚠️ Using the shared sample sheet. Set the GSHEET_URL environment variable "
            "or public_gsheet_url in Streamlit secrets to save your own data."
        )

    _conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    return _conn


def init_db():
    """Populate the sheet with initial data if it's empty."""
    conn = _init_connection()
    df = conn.read(spreadsheet=_sheet_url, worksheet=_SHEET_NAME, ttl=0)
    if df.empty and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype={"聯絡電話": str})
        if _writing_enabled():
            conn.update(worksheet=_SHEET_NAME, data=df)


def get_all_locations():
    conn = _init_connection()
    df = conn.read(spreadsheet=_sheet_url, worksheet=_SHEET_NAME, ttl=0)
    if df.empty:
        df = pd.DataFrame(
            columns=["工地名稱", "地址", "GoogleMap網址", "工地主任", "聯絡電話"]
        )
    df.insert(0, "id", range(2, len(df) + 2))
    return df


def add_location(name, address, url, supervisor, phone):
    conn = _init_connection()
    df = conn.read(spreadsheet=_sheet_url, worksheet=_SHEET_NAME, ttl=0)
    new_row = {
        "工地名稱": name,
        "地址": address,
        "GoogleMap網址": url,
        "工地主任": supervisor,
        "聯絡電話": phone,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    if _writing_enabled():
        conn.update(worksheet=_SHEET_NAME, data=df)
    else:
        st.warning(
            "Data not saved because the default shared sheet is read-only. "
            "Set GSHEET_URL or public_gsheet_url to enable editing."
        )


def delete_location(row_id):
    conn = _init_connection()
    df = conn.read(spreadsheet=_sheet_url, worksheet=_SHEET_NAME, ttl=0)
    idx = int(row_id) - 2
    if 0 <= idx < len(df):
        df = df.drop(df.index[idx]).reset_index(drop=True)
        if _writing_enabled():
            conn.update(worksheet=_SHEET_NAME, data=df)
        else:
            st.warning(
                "Data not deleted because the default shared sheet is read-only. "
                "Set GSHEET_URL or public_gsheet_url to enable editing."
            )
