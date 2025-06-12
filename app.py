import io, os
import streamlit as st
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

st.set_page_config(page_title="SharePoint Excel Viewer", layout="wide")

# ---------------------------------------------------------------------------
# ❶ Read secrets / env-vars (→ nothing shown in the UI)
# ---------------------------------------------------------------------------
SITE_URL   = os.getenv("SP_SITE_URL",   st.secrets.get("sp_site_url",   ""))
FILE_ID    = os.getenv("SP_FILE_ID",    st.secrets.get("sp_file_id",    ""))
FILE_NAME  = os.getenv("SP_FILE_NAME",  st.secrets.get("sp_file_name",  ""))
SHEET_NAME = os.getenv("SP_SHEET_NAME", st.secrets.get("sp_sheet_name", "Marketplace 25"))
USERNAME   = os.getenv("SP_USERNAME",   st.secrets.get("sp_username",   ""))
PASSWORD   = os.getenv("SP_PASSWORD",   st.secrets.get("sp_password",   ""))

# ---------------------------------------------------------------------------
st.title("📊 SharePoint workbook viewer")
load_btn = st.button("Load workbook")

@st.cache_data(show_spinner="Downloading & parsing workbook…")
def fetch_sheet():
    ctx   = ClientContext(SITE_URL).with_credentials(UserCredential(USERNAME, PASSWORD))
    sp_file = ctx.web.get_file_by_id(FILE_ID)
    buf = io.BytesIO()
    sp_file.download(buf).execute_query()
    buf.seek(0)
    df = pd.read_excel(buf, sheet_name=SHEET_NAME, header=1, engine="openpyxl")
    cols = ['ORDEN DE COMPRA', 'REGIONAL', 'PROVEEDOR', 'ESTADO']
    return df[cols]

if load_btn:
    try:
        df = fetch_sheet()
        st.success(f"Loaded **{len(df):,}** rows from “{SHEET_NAME}”")
        st.dataframe(df, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"❌ {e}")
else:
    st.info("Click **Load workbook** to retrieve the data.")
