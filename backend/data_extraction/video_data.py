import pandas as pd
import isodate

from backend.api.youtube_client import get_youtube_client


def get_video_data(channel_id):
    youtube = get_youtube_client()

    # Step 1: Get Upload Playlist ID
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    if not channel_response["items"]:
        return pd.DataFrame()

    uploads_playlist_id = channel_response["items"][0]\
        ["contentDetails"]["relatedPlaylists"]["uploads"]

    # Step 2: Get Video IDs from Upload Playlist
    video_ids = []

    playlist_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50
    )

    playlist_response = playlist_request.execute()

    for item in playlist_response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    if not video_ids:
        return pd.DataFrame()

    # Step 3: Fetch Video Details
    video_response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()

    video_data = []

    for item in video_response["items"]:

        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        content = item.get("contentDetails", {})

        # 🔥 FIXED DURATION CONVERSION
        duration_iso = content.get("duration", "PT0S")

        try:
            duration_seconds = int(
                isodate.parse_duration(duration_iso).total_seconds()
            )
        except:
            duration_seconds = 0

        video_data.append({
            "video_id": item.get("id"),
            "channel_id": channel_id,
            "title": snippet.get("title"),
            "views": int(statistics.get("viewCount", 0)),
            "likes": int(statistics.get("likeCount", 0)),
            "comments": int(statistics.get("commentCount", 0)),
            "duration": duration_seconds,
            "published_date": snippet.get("publishedAt")
        })

    return pd.DataFrame(video_data)