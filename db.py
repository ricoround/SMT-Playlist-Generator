import sqlite3

def connect_to_db_songid():
    """
    Connects to the database and returns the connection and cursor objects

    :return: connection, cursor
    """
    conn = sqlite3.connect("songid.sqlite")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS songid (id TEXT PRIMARY KEY, title TEXT)"""
    )
    conn.commit()
    return conn, cursor