import pandas
import urllib
import utm

# utm zone:50 j
df = pandas.read_csv(
    "/home/rglsm/Codes/UWA_CEED_Web/csv/stops20090101 - 20090228.csv")

for index, row in df.iterrows():

    if row['STATUS'] != 'Discontinued':
        latlon = ()
        station_name = (row['ROAD'] if not pandas.isnull(row['ROAD']) else '') + ' ' + (row['SUFFIX'] if not pandas.isnull(row['SUFFIX']) else '') + \
            ' ' + (row['STOPNAME'] if not pandas.isnull(row['STOPNAME']) else '') + \
            ' ' + (row['SUBURB'] if not pandas.isnull(row['SUBURB']) else '')
        print(station_name)
        if not pandas.isnull(row['POSITIONX_MGA']):
            if row['POSITIONX_MGA'] < 10000:
                latlon = (row['POSITIONY_MGA'], row['POSITIONX_MGA'])
            else:
                latlon = utm.to_latlon(row['POSITIONX_MGA'], row[
                    'POSITIONY_MGA'], 50, 'J')
            df.set_value(index, "lat", latlon[0])
            df.set_value(index, "lon", latlon[1])
            df.set_value(index, 'FULLNAME', station_name)

df.to_csv('./stops20090101 - 20090228_latlon.csv')
