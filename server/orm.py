def get_lat_lon(row):
    # return tuple(lat,lon), if not found then return None(disabled bus route)
    if pandas.isnull(row['lat']) or pandas.isnull(row['lon']):
        return None
    return (row['lat'], row['lon'])


def getRouteJson(on, off, key):
    url_origin = 'https://maps.googleapis.com/maps/api/directions/json?'
    stops_df = pandas.read_csv('./stops_latlon_placeid.csv')
    combinations_df = pandas.read_csv('./routeCombinations.csv')
    stops_df = stops_df.set_index('STOPNUMBER')
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
