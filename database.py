import sqlite3
import pandas as pd

DB_NAME = "youtube_data.db"


# ================= DATABASE CONNECTION =================
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


# ================= CREATE TABLES =================
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # CHANNEL TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        channel_id TEXT PRIMARY KEY,
        channel_name TEXT,
        subscribers INTEGER,
        views INTEGER,
        total_videos INTEGER
    )
    """)

    # VIDEO TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        video_id TEXT PRIMARY KEY,
        channel_id TEXT,
        title TEXT,
        published_date TEXT,
        views INTEGER,
        likes INTEGER,
        comments INTEGER,
        duration TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= INSERT CHANNEL DATA =================
def insert_channel(df):

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            "SELECT channel_id FROM channels WHERE channel_id=?",
            (row["channel_id"],)
        )

        result = cursor.fetchone()

        # Prevent duplicate channel insert
        if result is None:

            cursor.execute("""
            INSERT INTO channels (
                channel_id,
                channel_name,
                subscribers,
                views,
                total_videos
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                row["channel_id"],
                row["channel_name"],
                row["subscribers"],
                row["views"],
                row["total_videos"]
            ))

    conn.commit()
    conn.close()


# ================= INSERT VIDEO DATA =================
def insert_videos(df):

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            "SELECT video_id FROM videos WHERE video_id=?",
            (row["video_id"],)
        )

        result = cursor.fetchone()

        # Prevent duplicate videos
        if result is None:

            cursor.execute("""
            INSERT INTO videos (
                video_id,
                channel_id,
                title,
                published_date,
                views,
                likes,
                comments,
                duration
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["video_id"],
                row["channel_id"],
                row["title"],
                row["published_date"],
                row["views"],
                row["likes"],
                row["comments"],
                row["duration"]
            ))

    conn.commit()
    conn.close()


# ================= GET ALL CHANNELS =================
def get_all_channels():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM channels",
        conn
    )

    conn.close()

    return df


# ================= GET ALL VIDEOS =================
def get_all_videos():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM videos",
        conn
    )

    conn.close()

    return df