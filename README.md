# YouTube Channel Performance and Engagement Analytics Dashboard

A Streamlit-based analytics dashboard that connects to the YouTube Data API to fetch, store, and analyze channel and video performance data — with interactive filters, visualizations, exports, and multi-channel comparison.

🔗 **Live Demo:** [https://larasamynathan-youtube-analytic-dashboard.streamlit.app/](https://larasamynathan-youtube-analytic-dashboard.streamlit.app/)

---

## Overview
This dashboard connects to the YouTube Data API to fetch channel and video details, stores them in a SQLite database, and presents them through an interactive Streamlit interface. Users can pull data for any channel using its Channel ID, explore it through rich filters, visualize performance trends, compare channels side by side, and export results for offline analysis.

## Features
- Connects to the YouTube Data API and extracts channel details — name, subscriber count, total views, and total video count
- Fetches and stores video-level data (views, likes, comments, duration, publish date) for any channel using its Channel ID
- Persists all fetched data in a SQLite database, with the ability to view all stored channels and videos at any time
- Cleans and processes raw API data — parsing ISO 8601 video durations into seconds, converting numeric fields, handling nulls, and normalizing timezones
- Summarizes key dashboard metrics: total videos, total views, total likes, total comments, and average engagement rate
- Offers a multi-filter sidebar to narrow down videos by title search, views range, duration range, comments range, minimum engagement rate, and publish date range
- Displays filtered results in a paginated, sortable table
- Exports filtered data as CSV or Excel for offline use
- Visualizes analytics through selectable charts — Top Viewed Videos, Most Liked Videos, Monthly Upload Trend, Top Engagement, Channel Video Count, and Top Commented Videos
- Ranks channels on a Leaderboard by subscriber count
- Enables side-by-side Channel Comparison of subscribers across selected channels
- Generates an Engagement Correlation heatmap across views, likes, comments, and engagement rate
- Includes a built-in Help section walking through how to use the dashboard

---

## Technologies Used
- **Python**
- **Streamlit** — web app framework
- **YouTube Data API** — data source
- **Pandas** — data processing
- **Matplotlib** — charts and visualizations
- **SQLite** — data storage
- **openpyxl** — Excel export support
- **python-dotenv** — environment variable management

---

## Project Structure
```
├── app/                  # YouTube API integration logic
├── backend/              # Backend utilities
├── database.py           # Database creation & CRUD operations
├── streamlit_app.py       # Main Streamlit dashboard
├── test_database.py       # Database tests
├── view_db.py             # Database inspection utility
├── youtube.db              # SQLite database (channels/videos)
├── requirements.txt        # Project dependencies
└── README.md
```

---

## How to Run the Project Locally

1. Clone the repository:
   ```
   git clone https://github.com/larasamynathan/youtube-analytic-dashboard.git
   cd youtube-analytic-dashboard
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Add your YouTube Data API key to a `.env` file:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   streamlit run streamlit_app.py
   ```

---

## How to Use
1️⃣ Enter a YouTube Channel ID in the sidebar
2️⃣ Click **Fetch Channel Data**
3️⃣ Click **Store Data** to save it to the database
4️⃣ Use the sidebar filters to narrow down videos
5️⃣ Explore analytics, leaderboard, and comparison charts
6️⃣ Export results as CSV or Excel

---

## Live Deployment
This app is deployed on **Streamlit Community Cloud**:
🔗 [https://larasamynathan-youtube-analytic-dashboard.streamlit.app/](https://larasamynathan-youtube-analytic-dashboard.streamlit.app/)



