import mysql.connector
import pandas

conn = mysql.connector.connect(
    user='root', password='7655558', database='ceed')
cursor = conn.cursor()
cursor.execute('select distinct OnLandmark,OffLandmark from journey;')
bus_result = cursor.fetchall()
cursor.execute(
    'select distinct OnLocation,OffLocation from journey where OnLocation>=1000 and OffLocation >=1000;')
train_result = cursor.fetchall()


cursor.close()
for i in range(len(bus_result) - 1, -1, -1):
    if not bus_result[i][0] or not bus_result[i][1]:
        del bus_result[i]

all_result = bus_result + train_result
df = pandas.DataFrame({'On': list(map(lambda x: x[0], all_result)),
                       'Off': list(map(lambda x: x[1], all_result))})
df.to_csv('./routeCombinations.csv', index=False)
