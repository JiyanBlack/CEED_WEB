import mysql.connector
import pandas


def get_on_off():
    conn = mysql.connector.connect(
        user='root', password='7655558', database='ceed')
    query_info = None  # tupple(CardId,BeginOnDay,EndOffDay)
    while True:
        if query_info:
            cursor = conn.cursor()
            cursor.execute(
                'select OnLandmark,OffLandmark from journey where CardId=' + str(query_info[0]))
            query_info = yield cursor.fetchall()
            cursor.close()
        else:
            query_info = yield None


def get_coordinates():
    # get list[tuple(start,end,Bool isPlaceId)]
    on_off = get_on_off()
    on_off.send(None)
    result = on_off.send((914194, '', ''))
    for j in range(len(result) - 1, -1, -1):
        if result[j][0] == 0 or result[j][1] == 0:
            del result[j]
    print(result)

get_coordinates()
