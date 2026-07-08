from database import *
import pandas as pd

# Create tables first
create_tables()

# -------------------------
# Insert Channel 1
# -------------------------
channel_1 = {
    "channel_id": "UC001",
    "channel_name": "Tech World",
    "subscribers": 10000,
    "total_views": 500000,
    "total_videos": 50,
    "created_at": "2020-01-01"
}

insert_or_update_channel(channel_1)

# -------------------------
# Insert Channel 2
# -------------------------
channel_2 = {
    "channel_id": "UC002",
    "channel_name": "Code Master",
    "subscribers": 20000,
    "total_views": 800000,
    "total_videos": 80,
    "created_at": "2019-05-10"
}

insert_or_update_channel(channel_2)

# -------------------------
# Re-insert Channel 1 (Update test)
# -------------------------
channel_1_updated = {
    "channel_id": "UC001",
    "channel_name": "Tech World Updated",
    "subscribers": 15000,   # changed
    "total_views": 600000,  # changed
    "total_videos": 55,
    "created_at": "2020-01-01"
}

insert_or_update_channel(channel_1_updated)

print("Channels inserted and updated successfully!")

# -------------------------
# Insert Sample Videos
# -------------------------
video_data = pd.DataFrame([
    {
        "video_id": "VID001",
        "channel_id": "UC001",
        "title": "Python Tutorial",
        "views": 10000,
        "likes": 500,
        "comments": 50,
        "published_date": "2023-01-01"
    },
    {
        "video_id": "VID002",
        "channel_id": "UC001",
        "title": "AI Explained",
        "views": 20000,
        "likes": 1000,
        "comments": 120,
        "published_date": "2023-02-01"
    }
])

insert_videos(video_data)

print("Videos inserted successfully!")