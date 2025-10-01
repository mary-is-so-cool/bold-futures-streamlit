import pathlib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Bold Futures — Grant Matcher", layout="wide")
st.title("Bold Futures — Grant Matcher")

# --- Load data ---
DEFAULT_PATH = pathlib.Path("data/grants_normalized.csv")

df = None
status = st.empty()

colL, colR = st.columns([1, 3])
with colL:
    st.subheader("Data")
    data_path_str = st.text_input("CSV path (in repo)", value=str(DEFAULT_PATH))
    uploaded = st.file_uploader("...or upload a CSV", type=["csv"])

# Try uploaded file first; else try path
try:
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        status.success(f"Loaded {len(df)} rows from uploaded file.")
    else:
        p = pathlib.Path(data_path_str)
        if p.exists():
            df = pd.read_csv(p)
            status.success(f"Loaded {len(df)} rows from {p}")
        else:
            status.info("No CSV loaded yet. Upload a file or create data/grants_normalized.csv")
except Exception as e:
    status.error(f"Failed to load CSV: {e}")

# --- Show & filter ---
if df is not None and not df.empty:
    with colR:
        st.subheader("Preview & Filter")
        q = st.text_input("Search title/summary/keywords", value="")

        # Basic text filter
        if q.strip():
            mask = (
                df.get("title", "").astype(str).str.contains(q, case=False, na=False) |
                df.get("summary", "").astype(str).str.contains(q, case=False, na=False) |
                df.get("keywords", "").astype(str).str.contains(q, case=False, na=False)
            )
            filtered = df.loc[mask].copy()
        else:
            filtered = df.copy()

        st.write(f"Showing {len(filtered)} of {len(df)} total")
        st.dataframe(filtered, use_container_width=True)

        # Download filtered as CSV
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered CSV", data=csv_bytes, file_name="grants_filtered.csv")

        # Optional: show the first few as “cards”
        st.markdown("---")
        st.subheader("Top rows")
        for _, row in filtered.head(3).iterrows():
            with st.container(border=True):
                st.markdown(f"**{row.get('title','(no title)')}**")
                st.write(row.get("summary", ""))
                st.write(
                    f"Agency: {row.get('agency','')}  |  State: {row.get('state','')}  |  Deadline: {row.get('deadline_utc','')}"
                )
                url = str(row.get("opportunity_url","")).strip()
                if url and url.lower().startswith(("http://", "https://")):
                    st.link_button("Open Opportunity", url)
