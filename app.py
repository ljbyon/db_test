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
@st.cache_data(show_spinner="Downloading & parsing workbook…")
def fetch_sheet():
    # ------------- 0. Basic validation
    if not all([SITE_URL, USERNAME, PASSWORD]):
        raise ValueError("SITE_URL / USERNAME / PASSWORD must be provided")

    # ------------- 1. Connect
    ctx = ClientContext(SITE_URL).with_credentials(UserCredential(USERNAME, PASSWORD))

    # ------------- 2. Download (try GUID first, then path)
    buf = io.BytesIO()
    try:
        ctx.web.get_file_by_id(FILE_ID).download(buf).execute_query()
    except Exception as guid_err:
        # Fallback: assume the file lives in the default "Documents" library
        rel_url = f"/personal/eflores_dismac_com_bo/Documents/{FILE_NAME}"
        try:
            ctx.web.get_file_by_server_relative_url(rel_url).download(buf).execute_query()
        except Exception as path_err:
            raise RuntimeError(
                f"GUID lookup failed ({guid_err}) *and* path lookup failed ({path_err})."
            ) from None

    if buf.tell() == 0:
        raise RuntimeError("Downloaded file is 0 bytes – check FILE_ID / permissions.")

    # ------------- 3. Parse Excel
    buf.seek(0)
    df = pd.read_excel(buf, sheet_name=SHEET_NAME, header=1, engine="openpyxl")
    return df[['ORDEN DE COMPRA', 'REGIONAL', 'PROVEEDOR', 'ESTADO']]

if load_btn:
    try:
        df = fetch_sheet()
        st.success(f"Loaded **{len(df):,}** rows from “{SHEET_NAME}”")
        st.dataframe(df, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"❌ {e}")
else:
    st.info("Click **Load workbook** to retrieve the data.")
