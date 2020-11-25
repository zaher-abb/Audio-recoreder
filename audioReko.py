import requests  # to connect to url
import arrow  # to calculate time
import click  # to provide command line interface
import sqlite3  # to creat database
import os
import sys



@click.command()

@click.option('--duration')
@click.option('--filename')
@click.option('--split-count')
@click.option('--url')
@click.option("-l",is_flag=True)
def get_stream(l,url, duration=30, filename='myRadio.mp3', split_count=2):
    if l:
        for item in fetch_all_records():
            print(f"url:{item[0]} duration:{item[1]} file:{item[2]}")
        sys.exit()
    duration = int(duration)
    split_count = int(split_count)
    stream_duration = (duration / split_count) - 2
    file_name_list = []
    for count in range(1, split_count + 1):
        current_time = arrow.now().timestamp
        r = requests.get(url, stream=True)
        chunk_file = "{}{}.mp3".format(filename, count)
        f1 = open(chunk_file, "wb")
        file_name_list.append(chunk_file)
        # account for time required to load the stream
        for chunk in r.iter_content(chunk_size=512):
            f1.write(chunk)
            if arrow.now().timestamp - current_time >= stream_duration:
                f1.close()
                chunk_duration = int(duration / split_count)
                insert_record(url, chunk_duration, chunk_file)
                break


def insert_record(url, duration, filename):
    db = sqlite3.connect("db_1.sqlite")
    cur = db.cursor()
    query = ("INSERT INTO audio(url,duration,name) values(?,?,?) ")
    cur.execute(query, (url, duration, filename))
    db.commit()




def fetch_all_records():
    db = sqlite3.connect('db_1.sqlite')
    cur = db.cursor()
    cur.execute("select * from audio")
    return cur.fetchall()


# Creat Tabel
def creattabel(db):
    c = db.cursor()
    c.execute(''' 
                    CREATE TABLE audio(
                        url TEXT,
                        duration INTEGER,
                        name varchar(30));
                ''')
    db.commit()


if __name__ == "__main__":
    if os.path.exists("db_1.sqlite") == False:
        db_name = "db_1.sqlite"
        db = sqlite3.connect(db_name)
        creattabel(db)


    get_stream()

    # get_stream(6, 'https://wdr-edge-10b6-fra-dtag-cdn.cast.addradio.de/wdr/1live/diggi/mp3/128/stream.mp3', 'test', 3
    #            )


    #insert_record('myRadio', 390, url1)

    print("hello")
    '''records = fetch_all_records()
    for item in fetch_all_records():
        print(f" Filename: {item[0]}, duration: {item[1]}, url: {item[2]}")'''
