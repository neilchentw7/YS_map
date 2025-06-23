import streamlit as st
import base64
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 頁面設定
st.set_page_config(page_title="禹盛-工地導航系統", layout="wide")

# 讀取並顯示 Logo
def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

img_base64 = image_to_base64("logo.png")
st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 8px;'>
        <img src='data:image/png;base64,{img_base64}' width='40' style='margin:0;'/>
        <h2 style='margin:0;'>禹盛工地導航系統</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# 讀取 Google Sheet
service_account_info = json.loads(st.secrets["gcp"]["gcp_service_account"])
spreadsheet_id = st.secrets["gcp"]["spreadsheet_id"]

credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(spreadsheet_id).sheet1

rows = worksheet.get_all_records()
df = pd.DataFrame(rows, dtype=str)

# 顯示工地清單
st.subheader("📋 工地清單（依工地名稱首字分組）")
COLUMNS = ["工地名稱", "地址", "GoogleMap網址", "工地主任", "聯絡電話"]
if df.empty:
    df = pd.DataFrame(columns=COLUMNS)

df_display = df.copy()
df_display["首字"] = df_display["工地名稱"].str[0]
for key in sorted(df_display["首字"].unique()):
    group = df_display[df_display["首字"] == key]
    st.markdown(f"### {key}")
    for idx, row in group.iterrows():
        col1, _, col3 = st.columns([6, 1, 1])
        with col1:
            st.markdown(
                f"**{row['工地名稱']}**  |  {row['地址']}<br>"
                f"[📍 導航]({row['GoogleMap網址']})<br>"
                f"👷 {row['工地主任']}  📞 {row['聯絡電話']}",
                unsafe_allow_html=True,
            )
        with col3:
            if st.button("刪除", key=f"del_{idx}"):
                worksheet.delete_rows(idx + 2)
                st.experimental_rerun()
        st.markdown(
            "<hr style='border-top:1px dashed lightgray;'>",
            unsafe_allow_html=True,
        )

# 搜尋功能
st.subheader("🔍 查詢工地")
search = st.text_input("輸入關鍵字")
if search:
    filtered = df[df.apply(lambda r: search in r.to_string(), axis=1)]
    st.write(f"🔎 查詢結果：{len(filtered)} 筆")
    st.dataframe(filtered)

# ➕ 新增工地
with st.expander("➕ 新增工地資料"):
    with st.form("add_form"):
        name = st.text_input("工地名稱")
        address = st.text_input("地址")
        url = st.text_input("Google Map 導航連結")
        supervisor = st.text_input("工地主任姓名")
        phone = st.text_input("聯絡電話")
        submit = st.form_submit_button("新增")
        if submit:
            if name and url:
                worksheet.append_row([name, address, url, supervisor, phone])
                st.success("✅ 已新增工地")
                st.experimental_rerun()
            else:
                st.error("❌ 請填寫工地名稱與 Google Map 連結")
