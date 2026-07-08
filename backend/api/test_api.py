from youtube_api import get_youtube_service

youtube = get_youtube_service()

request = youtube.channels().list(
    part="snippet,statistics",
    forUsername="GoogleDevelopers"
)

response = request.execute()

print("Channel Name:", response["items"][0]["snippet"]["title"])
print("Subscribers:", response["items"][0]["statistics"]["subscriberCount"])
