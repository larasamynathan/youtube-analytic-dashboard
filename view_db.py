import sqlite3
import pandas as pd

conn = sqlite3.connect("youtube_analytics.db")

channels = pd.read_sql("SELECT * FROM channels", conn)
videos = pd.read_sql("SELECT * FROM videos", conn)

print("CHANNELS TABLE")
print(channels)

print("\nVIDEOS TABLE")
print(videos)

conn.close()
