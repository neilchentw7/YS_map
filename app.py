
import streamlit as st
import base64
import pandas as pd
import os

# 頁面設定
st.set_page_config(page_title="禹盛-工地導航系統", layout="wide")

# 將 logo.png 轉成 base64 編碼，以內嵌方式顯示
def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

img_base64 = image_to_base64("logo.png")

# 使用 HTML 緊貼顯示 logo 與標題
st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 8px;'>
        <img src='data:image/png;base64,{img_base64}' width='40' style='margin: 0;'/>
        <h2 style='margin: 0;'>禹盛工地導航系統</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 資料庫檔案位置
DB_PATH = "site_locations.csv"
# 刪除密碼
DELETE_PASSWORD = "27880751"

# 讀取資料
if os.path.exists(DB_PATH):    
    df = pd.read_csv(DB_PATH, dtype={"聯絡電話": str})

else:
    df = pd.DataFrame(columns=["工地名稱", "地址", "GoogleMap網址", "工地主任", "聯絡電話"])

# 📋 顯示工地資料（使用副本加上首字）
st.subheader("📋 工地清單（依工地名稱首字分組）")

df_display = df.copy()
df_display['首字'] = df_display['工地名稱'].str[0]
grouped = df_display.groupby('首字')

for group_key in sorted(grouped.groups.keys()):
    group = grouped.get_group(group_key)
    for idx, row in group.iterrows():
        col1, col2, col3 = st.columns([6, 3, 1])
        with col1:
            st.markdown(
                f"**{row['工地名稱']}**<br>"
                f"[📍 開啟 Google Map 導航]({row['GoogleMap網址']})<br>"
                f"{row['地址']}<br>"
                f"👷 主任：{row['工地主任']}<br>"
                f"📞 電話：{row['聯絡電話']}",
                unsafe_allow_html=True
            )
        with col3:
            confirm_key = f"confirm_{row.name}"
            pwd_key = f"pwd_{row.name}"
            if st.session_state.get(confirm_key):
                pwd = st.text_input("刪除密碼", type="password", key=pwd_key)
                if st.button("確認刪除", key=f"confirm_del_{row.name}"):
                    if pwd == DELETE_PASSWORD:
                        df = df.drop(row.name).reset_index(drop=True)
                        df.to_csv(DB_PATH, index=False)
                        st.experimental_rerun()
                    else:
                        st.error("❌ 密碼錯誤，未進行刪除")
                    st.session_state.pop(confirm_key)
                    st.session_state.pop(pwd_key, None)
            else:
                if st.button("刪除", key=f"del_{row.name}"):
                    st.session_state[confirm_key] = True

        # 🔹 加上淺灰色虛線分隔線
        st.markdown("<hr style='border-top: 1px dashed lightgray;'>", unsafe_allow_html=True)

# 🔍 搜尋工地
st.subheader("🔍 查詢工地")
search = st.text_input("輸入工地名稱、地址、主任或電話關鍵字查詢")
if search:
    filtered_df = df[df.apply(lambda row: search in row.to_string(), axis=1)]
    st.write("🔎 查詢結果：", len(filtered_df), "筆")
    for idx, row in filtered_df.iterrows():
        st.markdown(
            f"**{row['工地名稱']}** | {row['地址']} | 👷 {row['工地主任']} | 📞 {row['聯絡電話']} | "
            f"[導航]({row['GoogleMap網址']})",
            unsafe_allow_html=True
        )

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
                df.loc[len(df)] = [name, address, url, supervisor, phone]
                df.to_csv(DB_PATH, index=False)
                st.success("✅ 已新增工地")
                st.experimental_rerun()
            else:
                st.error("❌ 請填寫工地名稱與 Google Map 連結")
