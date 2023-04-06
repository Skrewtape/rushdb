#!python

import csv
import datetime
import os

from mysql.connector import connect

insert_album = (
    "INSERT INTO albums "
    "(title, release_date, url) VALUES "
    "(%s, %s, %s)"
)

insert_song = (
    "INSERT INTO songs "
    "(name, album_order, album_id, url) VALUES "
    "(%s, %s, %s, %s)"
)

with connect(
    host='localhost',
    database='RushDB',
    user=os.environ['mysql_user'],
    password=os.environ['mysql_password'],
) as connection:
    with connection.cursor() as cursor:
        with open('data/discography.csv') as csvfile:
            r = csv.reader(csvfile)
            album_id = None
            for row in r:
                if row[0] == 'Release Date':
                    # Header, skip
                    continue
                if row[0] != '':
                    # This is an album
                    cursor.execute(
                        insert_album,
                        (row[1], datetime.datetime.strptime(row[0], "%m/%d/%Y"), row[2] or None)
                    )
                    album_id = cursor.lastrowid
                    album_order = 0
                    connection.commit()
                else:
                    # This is a song
                    cursor.execute(
                        insert_song,
                        (row[3], album_order, album_id, row[4] or None)
                    )
                    album_order += 1
                    connection.commit()
