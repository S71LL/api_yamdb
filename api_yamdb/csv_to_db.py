"""
Этот скрипт написан для преобразования
данных из *.csv файлов в записи db.sqlite3
"""
import sqlite3
import csv
import os, glob

path = '/static/data/'
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
for filename in glob.glob(os.path.join(path, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['cert_time'], i['cfthostname'], i['cftshortname'], i['cftenv'], ) for i in dr]

        cursor.executemany(
            "UPDATE itpassed_host SET cert_time = ? WHERE cfthostname = ? AND cftshortname = ? AND cftenv = ?", to_db
        )
        conn.commit()

        conn.close()
