for k in ("SP_SITE_URL","SP_FILE_ID","SP_USERNAME","SP_PASSWORD"):
    assert os.getenv(k, st.secrets.get(k.lower(),"")), f"{k} is missing"