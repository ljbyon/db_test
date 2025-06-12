import sqlite3
import streamlit as st

DB_PATH = "data.db"

# ---------- tiny “DB layer” ----------
@st.experimental_singleton  # one connection per session
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)"
    )
    return conn

def add_note(text: str):
    with get_conn() as conn:
        conn.execute("INSERT INTO notes (content) VALUES (?)", (text,))

def fetch_note(note_id: int):
    row = get_conn().execute("SELECT content FROM notes WHERE id = ?", (note_id,)).fetchone()
    return None if row is None else row[0]

# ---------- Streamlit UI ----------
st.title("📓 Minimal Streamlit + SQLite demo")

# --- write ---
with st.form("add"):
    new_text = st.text_input("Write something")
    if st.form_submit_button("Save note") and new_text:
        add_note(new_text)
        st.success("Saved!")

st.divider()

# --- read ---
note_id = st.number_input("Retrieve note #", min_value=1, step=1, format="%d")
if st.button("Fetch"):
    result = fetch_note(note_id)
    if result:
        st.info(f"→ {result}")
    else:
        st.warning("Nothing stored under that ID.")
