import streamlit as st
from src.data_extraction.channel_data import get_channel_data

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="YouTube Channel Analytics",
    layout="centered"
)

# ---------------------------------------------------
# App Title & Description
# ---------------------------------------------------
st.title("📊 YouTube Channel Analytics Dashboard")

st.write(
    "Enter a **YouTube Channel ID** below to fetch basic channel performance "
    "metrics such as subscribers, views, and total videos."
)

st.markdown("---")

# ---------------------------------------------------
# Channel ID Input
# ---------------------------------------------------
channel_id = st.text_input(
    "YouTube Channel ID",
    placeholder="Example: UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

# ---------------------------------------------------
# Fetch Button
# ---------------------------------------------------
fetch_button = st.button("Fetch Channel Data")

# ---------------------------------------------------
# Button Click Logic
# ---------------------------------------------------
if fetch_button:
    if channel_id.strip() == "":
        st.error("❌ Please enter a valid YouTube Channel ID.")
    else:
        with st.spinner("Fetching channel data..."):
            df = get_channel_data(channel_id)

        if df.empty:
            st.error("⚠️ No data found. Please check the Channel ID and try again.")
        else:
            st.success("✅ Channel data fetched successfully!")

            # ---------------------------------------------------
            # Display Channel Information
            # ---------------------------------------------------
            st.image(df.loc[0, "thumbnail_url"], width=120)

            st.subheader(df.loc[0, "channel_name"])
            st.write(df.loc[0, "description"])

            st.markdown("### 📈 Channel Statistics")

            col1, col2, col3 = st.columns(3)

            col1.metric("Subscribers", df.loc[0, "subscribers"])
            col2.metric("Total Views", df.loc[0, "total_views"])
            col3.metric("Total Videos", df.loc[0, "video_count"])
