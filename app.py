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

missing = [k for k in ("SP_SITE_URL", "SP_FILE_ID", "SP_USERNAME", "SP_PASSWORD")
           if not os.getenv(k) and not st.secrets.get(k.lower(), "")]

if missing:
    st.error(f"The following secrets / env-vars are not set: {', '.join(missing)}")
    st.stop()
