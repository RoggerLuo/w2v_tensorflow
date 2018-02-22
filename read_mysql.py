from main import Task
import os
import mysql.connector
t = Task()


def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute('select * from flow_item')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

for x in range(20):
    notes = readNotes()
    length = len(notes)
    for i in range(length):
        content = notes[i][2]
        print('[第%d轮]' % x)
        print('    当前第%d段,一共%d段:' % ( i, length))
        trimmedContent = content.strip()
        print(trimmedContent[:10])
        t.readTxtLine(trimmedContent)


