from googleapiclient.discovery import build
import pandas as pd

# 🔑 PUT YOUR YOUTUBE API KEY HERE
API_KEY = "API KEY"

youtube = build("youtube", "v3", developerKey=API_KEY)


# ================= CHANNEL DATA =================
def get_channel_data(channel_id):

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )

    response = request.execute()

    if len(response["items"]) == 0:
        return pd.DataFrame()

    data = []

    for item in response["items"]:

        data.append({
            "channel_id": item["id"],
            "channel_name": item["snippet"]["title"],
            "subscribers": item["statistics"].get("subscriberCount", 0),
            "views": item["statistics"].get("viewCount", 0),
            "total_videos": item["statistics"].get("videoCount", 0)
        })

    return pd.DataFrame(data)


# ================= GET VIDEO IDS =================
def get_video_ids(channel_id):

    video_ids = []

    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date",
        type="video"
    )

    response = request.execute()

    for item in response["items"]:
        video_ids.append(item["id"]["videoId"])

    return video_ids


# ================= VIDEO DATA =================
def get_video_data(channel_id):

    video_ids = get_video_ids(channel_id)

    if not video_ids:
        return pd.DataFrame()

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )

    response = request.execute()

    videos = []

    for item in response["items"]:

        videos.append({
            "video_id": item["id"],
            "channel_id": channel_id,
            "title": item["snippet"]["title"],
            "published_date": item["snippet"]["publishedAt"],
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0),
            "duration": item["contentDetails"].get("duration", "PT0S")
        })

    return pd.DataFrame(videos)