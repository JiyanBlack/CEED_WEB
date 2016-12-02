from flask import Flask, url_for, send_from_directory, Response
import pandas
from pick_key import pick_key
import urllib
import json

app = Flask(__name__, static_url_path='/web/static')

stops_csv = pandas.read_csv('./csv/stops_latlon_placeid.csv')
user_csv = pandas.read_csv('./csv/20090228_with_date.csv')
stops_df = stops_csv.set_index('STOPNUMBER')


def get_placeid(row):
    # find place id or return None
    if pandas.isnull(row['status']) or row['status'] == 'ZERO_RESULTS':
        return None
    json_obj = json.loads(row['placeid_json'])
    return json_obj['results'][0]['place_id']


def get_lat_lon(row):
    # return tuple(lat,lon), if not found then return None(disabled bus route)
    if pandas.isnull(row['lat']) or pandas.isnull(row['lon']):
        return None
    return (row['lat'], row['lon'])


def encode_coord(info):
    if isinstance(info, tuple):
        # lat-lon coordinate
        return str(info[0]) + ',' + str(info[1])
    else:
        # place id
        return 'place_id:' + info


def getRouteJson(on, off, key):
    url_origin = 'https://maps.googleapis.com/maps/api/directions/json?'
    # get on/off row
    on_row = stops_df.loc[on]
    off_row = stops_df.loc[off]
    on_info = get_placeid(on_row) if get_placeid(
        on_row) else get_lat_lon(on_row)
    off_info = get_placeid(off_row) if get_placeid(
        off_row) else get_lat_lon(off_row)
    print(on_info, off_info)
    result = str(on_info) + ', ' + str(off_info)
    status = 'Place Id Error!'
    if on_info and off_info:
        parameters = {
            'origin': encode_coord(on_info),
            'destination': encode_coord(off_info),
            'key': key,
            'mode': 'transit',
            'transit_mode': 'bus',
            'language': 'en',
            'alternatives': 'true',
            'transit_routing_preference': 'fewer_transfers'
        }
        url = url_origin + urllib.parse.urlencode(parameters)
        try:
            with urllib.request.urlopen(url) as remote:
                result = remote.read().decode('utf-8')
                result_obj = json.loads(result)
                status = result_obj['status']
                result = json.dumps(result_obj, separators=(',', ':'))
        except Exception as e:
            status = 'Server Error!'
            result = str(e)
    return result, status


@app.route('/', methods=['GET'])
def root():
    return send_from_directory('web/static', 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    # send_static_file will guess the correct MIME type
    return send_from_directory('web/static/', path)


@app.route('/cardid/<int:id>/', methods=['GET'])
def get_user_json(id):
    bus_routes = []
    this_user = user_csv[user_csv['CardId'] == id]
    for index, row in this_user.iterrows():
        if not pandas.isnull(row['OnLandmark']) and not pandas.isnull(row['OffLandmark']):
            bus_routes.append((row['OnLandmark'], row['OffLandmark']))

    keys = pick_key()
    key = next(keys)
    final_json = []
    for route in bus_routes:
        on, off = route[0], route[1]
        result, status = getRouteJson(on, off, key)
        print("%s for %d to %d" % (status, on, off))
        while status == 'REQUEST_DENIED' or status == "OVER_QUERY_LIMIT":
            key = next(keys)
            result, status = getRouteJson(on, off, key)
        if status == 'OK':
            final_json.append(result)
    cur_res = Response(response=json.dumps(final_json),
                       status=200, mimetype="application/json")
    return cur_res

if __name__ == "__main__":
    app.run()
