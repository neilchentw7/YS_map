import streamlit as st
import base64
from streamlit_gsheets import GSheetsConnection

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


# 1) 把 edit#gid=0 換成 export?format=csv
CSV_URL = "https://docs.google.com/spreadsheets/d/1VV2AXV7-ZudWApvRiuKW8gcehXOM1CaPXGyHyFvDPQE/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(
    spreadsheet=CSV_URL,   # 直丟 URL -> 公開模式
    ttl="10m",             # 快取 10 分鐘
    header=0,              # 第 1 列當欄名
    on_bad_lines="skip"    # 若有壞行就跳過
)
st.dataframe(df)


# 顯示工地清單
st.subheader("📋 工地清單")
df_display = df.copy()
df_display['首字'] = df_display['工地名稱'].str[0]
for key, group in df_display.groupby('首字'):
    st.markdown(f"### {key}")
    for row in group.itertuples(index=False):
        col1, _, col3 = st.columns([6, 1, 1])
        with col1:
            st.markdown(
                f"**{row.工地名稱}**  |  {row.地址}<br>"
                f"[📍 導航]({row.GoogleMap網址})<br>"
                f"👷 {row.工地主任}  📞 {row.聯絡電話}",
                unsafe_allow_html=True,
            )
        st.markdown("<hr style='border-top:1px dashed lightgray;'>", unsafe_allow_html=True)

# 搜尋功能
st.subheader("🔍 查詢工地")
search = st.text_input("輸入關鍵字")
if search:
    filtered = df[df.apply(lambda r: search in r.to_string(), axis=1)]
    st.write(f"🔎 查詢結果：{len(filtered)} 筆")
    st.dataframe(filtered)
