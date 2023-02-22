#!/usr/bin/python3

import psycopg2

conn = psycopg2.connect(database="mydb", user="postgres", password="example",
                        host="127.0.0.1", port="5432")

# print(conn)

cur = conn.cursor()

cur.execute("select * from cities;")
rows = cur.fetchall()
for row in rows:
    print(row)

print("operation successful")

conn.close()

