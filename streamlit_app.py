import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

from app.youtube_api import get_channel_data, get_video_data
from database import (
    create_tables,
    insert_channel,
    insert_videos,
    get_all_channels,
    get_all_videos
)

# ================= PAGE CONFIG =================
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

st.title("📊 YouTube Channel Performance and Engagement Analytics Dashboard")

# ================= DATABASE INIT =================
try:
    create_tables()
except Exception as e:
    st.error(f"Database Initialization Error: {e}")
    st.stop()


# ================= DURATION CONVERTER =================
def convert_duration_to_seconds(duration):

    if pd.isna(duration):
        return 0

    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, str(duration))

    if not match:
        return 0

    h = int(match.group(1)) if match.group(1) else 0
    m = int(match.group(2)) if match.group(2) else 0
    s = int(match.group(3)) if match.group(3) else 0

    return h * 3600 + m * 60 + s


# ================= SIDEBAR =================
st.sidebar.header("Channel Operations")

channel_id = st.sidebar.text_input("Enter Channel ID")

# ================= FETCH DATA =================
if st.sidebar.button("Fetch Channel Data"):

    if not channel_id:
        st.sidebar.warning("Please enter Channel ID")

    else:
        try:
            with st.spinner("Fetching data..."):

                channel_df = get_channel_data(channel_id)
                video_df = get_video_data(channel_id)

            if not channel_df.empty:

                st.session_state["channel_df"] = channel_df
                st.session_state["video_df"] = video_df

                st.success("Channel data fetched successfully")

            else:
                st.error("Invalid Channel ID")

        except Exception as e:
            st.error(f"API Error: {e}")


# ================= STORE DATA =================
if st.sidebar.button("Store Data"):

    if "channel_df" not in st.session_state:
        st.warning("Fetch data first")

    else:
        try:

            insert_channel(st.session_state["channel_df"])
            insert_videos(st.session_state["video_df"])

            st.success("Data stored successfully")
            st.rerun()

        except Exception as e:
            st.error(f"Database Insert Error: {e}")


# ================= VIEW STORED DATA =================
st.header("📁 Stored Data")

col1, col2 = st.columns(2)

with col1:
    if st.button("View Channels"):
        try:
            st.dataframe(get_all_channels())
        except:
            st.error("Unable to fetch channels")

with col2:
    if st.button("View Videos"):
        try:
            st.dataframe(get_all_videos().head(20))
        except:
            st.error("Unable to fetch videos")


# ================= LOAD DATA =================
@st.cache_data
def load_videos():
    return get_all_videos()

try:
    videos_df = load_videos()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

if videos_df.empty:
    st.warning("No videos found in database")
    st.stop()


# ================= DATA CLEANING =================
videos_df["duration_seconds"] = videos_df["duration"].apply(convert_duration_to_seconds)

videos_df["views"] = pd.to_numeric(videos_df["views"], errors="coerce")
videos_df["likes"] = pd.to_numeric(videos_df["likes"], errors="coerce")
videos_df["comments"] = pd.to_numeric(videos_df["comments"], errors="coerce")

videos_df = videos_df.fillna(0)
videos_df = videos_df[videos_df["views"] > 0]

videos_df["engagement_rate"] = (
    (videos_df["likes"] + videos_df["comments"]) / videos_df["views"]
)

# ✅ FIXED TIMEZONE ISSUE
videos_df["published_date"] = pd.to_datetime(
    videos_df["published_date"], errors="coerce"
).dt.tz_localize(None)

videos_df = videos_df.dropna(subset=["published_date"])


# ================= DASHBOARD METRICS =================
st.header("📊 Dashboard Metrics")

total_videos = len(videos_df)
total_views = int(videos_df["views"].sum())
total_likes = int(videos_df["likes"].sum())
total_comments = int(videos_df["comments"].sum())
avg_engagement = round(videos_df["engagement_rate"].mean(), 4)

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Total Videos", total_videos)
m2.metric("Total Views", total_views)
m3.metric("Total Likes", total_likes)
m4.metric("Total Comments", total_comments)
m5.metric("Avg Engagement", avg_engagement)


# ================= FILTERS =================
with st.sidebar:

    st.subheader("Filters")

    search = st.text_input("Search Video Title")

    min_views = int(videos_df["views"].min())
    max_views = int(videos_df["views"].max())

    view_range = st.slider("Views Range", min_views, max_views, (min_views, max_views))

    min_duration = int(videos_df["duration_seconds"].min())
    max_duration = int(videos_df["duration_seconds"].max())

    duration_range = st.slider("Duration", min_duration, max_duration, (min_duration, max_duration))

    min_comments = int(videos_df["comments"].min())
    max_comments = int(videos_df["comments"].max())

    comment_range = st.slider("Comments Range", min_comments, max_comments, (min_comments, max_comments))

    max_engagement = float(videos_df["engagement_rate"].max())

    engagement_threshold = st.slider("Minimum Engagement Rate", 0.0, max_engagement, 0.0)

    date_range = st.date_input("Date Range", [])


# ================= APPLY FILTER =================
filtered_df = videos_df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df["views"] >= view_range[0]) &
    (filtered_df["views"] <= view_range[1])
]

filtered_df = filtered_df[
    (filtered_df["duration_seconds"] >= duration_range[0]) &
    (filtered_df["duration_seconds"] <= duration_range[1])
]

filtered_df = filtered_df[
    (filtered_df["comments"] >= comment_range[0]) &
    (filtered_df["comments"] <= comment_range[1])
]

filtered_df = filtered_df[
    filtered_df["engagement_rate"] >= engagement_threshold
]

if len(date_range) == 2:

    filtered_df = filtered_df[
        (filtered_df["published_date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["published_date"] <= pd.to_datetime(date_range[1]))
    ]


# ================= RESULTS =================
st.write("Total Results:", len(filtered_df))

page_size = 20

page = st.number_input(
    "Page",
    min_value=1,
    max_value=max(1, len(filtered_df)//page_size + 1),
    step=1
)

start = (page - 1) * page_size
end = start + page_size

display_df = filtered_df.iloc[start:end]

st.dataframe(display_df)


# ================= EXPORT =================
st.subheader("⬇ Export Data")

csv = filtered_df.to_csv(index=False)

st.download_button("Download CSV", csv, "youtube_analytics.csv")

excel_buffer = BytesIO()

export_df = filtered_df.copy()
export_df.to_excel(excel_buffer, index=False)

st.download_button(
    "Download Excel",
    excel_buffer,
    "youtube_analytics.xlsx"
)


# ================= ANALYTICS =================
st.header("📈 Analytics")

analysis_option = st.selectbox(
    "Select Analysis",
    [
        "Top Viewed Videos",
        "Most Liked Videos",
        "Monthly Upload Trend",
        "Top Engagement",
        "Channel Video Count",
        "Top Commented Videos"
    ]
)

if analysis_option == "Top Viewed Videos":

    top = filtered_df.sort_values("views", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top["title"], top["views"])
    ax.invert_yaxis()
    st.pyplot(fig)


elif analysis_option == "Most Liked Videos":

    top = filtered_df.sort_values("likes", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top["title"], top["likes"])
    ax.invert_yaxis()
    st.pyplot(fig)


elif analysis_option == "Monthly Upload Trend":

    temp = filtered_df.copy()
    temp["month"] = temp["published_date"].dt.to_period("M")

    trend = temp.groupby("month").size()

    fig, ax = plt.subplots()
    trend.plot(ax=ax)
    st.pyplot(fig)


elif analysis_option == "Top Engagement":

    top = filtered_df.sort_values("engagement_rate", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top["title"], top["engagement_rate"])
    ax.invert_yaxis()
    st.pyplot(fig)


elif analysis_option == "Channel Video Count":

    channel_videos = (
        filtered_df.groupby("channel_id")
        .size()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    channel_videos.plot(kind="bar", ax=ax)
    st.pyplot(fig)


elif analysis_option == "Top Commented Videos":

    top = filtered_df.sort_values("comments", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top["title"], top["comments"])
    ax.invert_yaxis()
    st.pyplot(fig)


# ================= CHANNEL LEADERBOARD =================
st.header("🏆 Channel Leaderboard")

try:
    channels_df = get_all_channels()

    if not channels_df.empty:

        leaderboard = channels_df.sort_values("subscribers", ascending=False)

        st.dataframe(leaderboard)

        fig, ax = plt.subplots()
        ax.barh(leaderboard["channel_name"], leaderboard["subscribers"])
        ax.invert_yaxis()

        st.pyplot(fig)

except:
    st.warning("Leaderboard unavailable")


# ================= CHANNEL COMPARISON =================
st.header("📊 Channel Comparison")

try:
    channels_df = get_all_channels()

    if not channels_df.empty:

        selected = st.multiselect(
            "Select Channels",
            channels_df["channel_name"]
        )

        if len(selected) >= 2:

            compare = channels_df[
                channels_df["channel_name"].isin(selected)
            ]

            st.dataframe(compare)

            fig, ax = plt.subplots()
            ax.bar(compare["channel_name"], compare["subscribers"])

            st.pyplot(fig)

except:
    st.warning("Comparison unavailable")


# ================= CORRELATION =================
st.header("📊 Engagement Correlation")

corr_df = filtered_df[["views", "likes", "comments", "engagement_rate"]]

corr = corr_df.corr()

fig, ax = plt.subplots()

cax = ax.matshow(corr)

fig.colorbar(cax)

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))

ax.set_xticklabels(corr.columns, rotation=45)
ax.set_yticklabels(corr.columns)

st.pyplot(fig)


# ================= HELP =================
st.header("❓ Help")

st.markdown("""
### Steps

1️⃣ Enter YouTube Channel ID  
2️⃣ Click Fetch Channel Data  
3️⃣ Store Data  
4️⃣ Apply Filters  
5️⃣ Explore Analytics  
6️⃣ Export Reports
""")