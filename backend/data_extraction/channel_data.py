import pandas as pd
from backend.api.youtube_client import get_youtube_client

def get_channel_data(channel_id):

    youtube = get_youtube_client()

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )

    response = request.execute()

    if not response["items"]:
        return pd.DataFrame()

    channel_info = response["items"][0]

    data = {
        "channel_id": channel_id,
        "channel_name": channel_info["snippet"]["title"],
        "subscribers": int(channel_info["statistics"].get("subscriberCount", 0)),
        "total_views": int(channel_info["statistics"].get("viewCount", 0)),
        "total_videos": int(channel_info["statistics"].get("videoCount", 0))
    }

    return pd.DataFrame([data])