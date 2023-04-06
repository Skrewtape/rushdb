#!python

import datetime
import os

from lxml import html

from mysql.connector import connect

insert_tour = "INSERT INTO tours (name) VALUES (%s)"
insert_venue = "INSERT INTO venues (name, city) VALUES (%s, %s)"
insert_tourdate = "INSERT INTO tourdates (tour_id, venue_id, performance_date) VALUES (%s, %s, %s)"

venues = {}

with connect(
    host='localhost',
    database='RushDB',
    user=os.environ['mysql_user'],
    password=os.environ['mysql_password'],
) as connection:
    with connection.cursor() as cursor:
        root = html.parse("data/tourdates.html")
        r = root.xpath('//*[self::h5 or self::table]')
        for h in r[2:]:
            if h.tag == 'h5':
                cursor.execute(insert_tour, (h.text_content(),))
                tour_id = cursor.lastrowid
                connection.commit()
            elif h.tag == 'table':
                for row in h[1:]:
                    try:
                        performance_date = datetime.datetime.strptime(
                            row[0].text_content(), "%B %d, %Y"
                        )
                    except ValueError:
                        continue
                    venue = tuple([row[x].text_content().strip() for x in (1, 2)])
                    venue_key = tuple([val.upper() for val in venue])
                    if 'UNKNOWN VENUE' in venue_key[0]:
                        continue
                    if venue_key in venues:
                        venue_id = venues[venue_key]
                    else:
                        cursor.execute(insert_venue, venue)
                        venue_id = cursor.lastrowid
                        venues[venue_key] = venue_id
                        connection.commit()
                    cursor.execute(insert_tourdate, (tour_id, venue_id, performance_date))
                    connection.commit()
