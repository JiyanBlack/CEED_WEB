from placeIDCrawler import pick_key
import json
import pandas
import urllib
from datetime import datetime


# def get_placeid(row):
#     # find place id or return None
#     if pandas.isnull(row['status']) or row['status'] == 'ZERO_RESULTS':
#         return None
#     json_obj = json.loads(row['placeid_json'])
#     return json_obj['results'][0]['place_id']

url_origin = 'https://maps.googleapis.com/maps/api/directions/json?'
stops_df = pandas.read_csv('../csv/stops_latlon_placeid.csv')
stops_df = stops_df.set_index('STOPNUMBER')


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


def process_json(result):
    # {
    #      "departure_stop":
    #      {
    #          "name": "Elizabeth Quay",
    #          "location": {"lat": -32, "lng": 115}
    #      },
    #       "arrival_stop":...
    #      }
    #      "routes":
    #       [{"name": "950",
    #        "polyline": "sadsvwea","type":"BUS"},....]
    # }
    routes = result["routes"]
    possible_routes = []
    possbile_route_found = False
    departure_stop = "NOT_FOUND"
    arrival_stop = "NOT_FOUND"
    for i in range(0, len(routes)):
        cur_route = routes[i]
        cur_route_transite_num = 0
        for leg in cur_route['legs']:
            for step in leg['steps']:
                if step['travel_mode'] == 'TRANSIT':
                    transit_step = step
                    cur_route_transite_num += 1
        if cur_route_transite_num == 1:
            if not possbile_route_found:
                departure_stop = transit_step[
                    'transit_details']['departure_stop']
                arrival_stop = transit_step['transit_details']['arrival_stop']
            if departure_stop == transit_step['transit_details']['departure_stop'] and arrival_stop == transit_step['transit_details']['arrival_stop']:
                transit_type = transit_step['transit_details'][
                    'line']['vehicle']['type']
                if transit_type == "BUS":
                    cur_line = transit_step['transit_details']['line']
                    potential_route = {"name": cur_line['short_name'] if 'short_name' in cur_line else cur_line['name'],
                                       "polyline": transit_step['polyline']
                                       }
                    possible_routes.append(potential_route)
    if len(possible_routes) == 0:
        return "NO_ROUTE", {}
    else:
        return "OK", {"departure_stop": departure_stop,
                      "arrival_stop": arrival_stop, "routes": possible_routes}


def get_json(on, off, key):
    global stops_df, url_origin, combinations_df

    # get on/off row
    on_row = stops_df.loc[on]
    off_row = stops_df.loc[off]
    on_info = get_lat_lon(on_row)
    off_info = get_lat_lon(off_row)
    result = str(on_info) + ', ' + str(off_info)
    status = 'PLACE_INFO_ERROR'
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
                result = json.loads(remote.read().decode('utf-8'))
                status = result['status']
        except Exception as e:
            status = 'SERVER_ERROR'
            result = str(e)
    return result, status

if __name__ == "__main__":
    counter = 0
    df = pandas.read_csv('./routes.csv')

    keys = pick_key()
    key = next(keys)

    first_time = "STATUS" not in df.columns
    for index, row in df.iterrows():
        if first_time or pandas.isnull(row['STATUS']) or (row['STATUS'] == 'SERVER_ERROR'):
            on, off = row['On'], row['Off']
            status = "UNINITIALIZED"  # status is uninitialized at first
            while status == 'REQUEST_DENIED' or status == "OVER_QUERY_LIMIT" or status == "UNINITIALIZED":
                if status == 'REQUEST_DENIED' or status == "OVER_QUERY_LIMIT":
                    key = next(keys)
                # update result and status
                result, status = get_json(on, off, key)
            if status == "OK":
                status, processed_result = process_json(result)
            df.ix[index, 'STATUS'] = status
            # save processed json string
            if status == "OK":
                minified_result_string = json.dumps(
                    processed_result, separators=(',', ':'))
                df.ix[index, 'ROUTES'] = minified_result_string
            print("%s for %d to %d, %d/%d" %
                  (status, on, off, counter, 66742))
            if counter % 100 == 99:
                df.to_csv('./routes.csv', index=False)
                print("===========> Saved at %d/%d <==========" %
                      (counter, 66742))
        counter += 1
    df.to_csv('./routes.csv', index=False)
    print("All Done!")
