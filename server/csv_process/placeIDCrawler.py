import pandas
import urllib
import json
import time
from datetime import datetime
import random


def pick_key():
    key_pool = [
        "AIzaSyDMwaHBaOiPQlKZgyKhuuuBz2LTXgkZs5o",
        "AIzaSyDg8lUiahxeP68SEeQklI4sTAQXOdmyEUQ",
        "AIzaSyCQqUTOyGb_Lzk_2jgfUTNswITr7USyenM",
        "AIzaSyAGgz_a8FVJySZigTNVXemc22rEfKITABs",
        "AIzaSyCT7p5M-QiFLdNVSQZ7g3imhUIVBvd1LGI",
        "AIzaSyDrFbVJx4QHEUy_LrG3H0sbaCqtzNYDWFc",
        "AIzaSyDPxAR82-3huRVwzs1Z8qHHXgvicyASS98",
        "AIzaSyAeSZDflSgsECfwg8CfCnwzkmgDUeScUlk",
        "AIzaSyCj-JvaXt6m7ko-Nq9BzlVT1dfmYAM5pE8",
        "AIzaSyArpqHUmePG2km3eMuCEUAFrEWDJTnnewM",
        "AIzaSyDY4mp03QM9_e-ouCkeBziZzHzr0K6zCbM",
        "AIzaSyAqpOEgC3t9p6fQbG48djvsGA3KCbyVNtc",
        "AIzaSyCkx_e6Xtmx691UklXLj3gpRd-KhTvZMAw",
        "AIzaSyA3QdMS3b2MdsNQFYnc3O6AGIV1LSRKEH4",
        "AIzaSyDMj9k4ReFMeyzlg_HEa02NdMX1dWN3f3A",
        "AIzaSyAa7wPbLFugvf9UtMQnnAhsraQJjZpbN58",
        "AIzaSyD1iNYWuCgUwfYh9f7YyyF7od-yUZ-p-0k",
        "AIzaSyCwEUq8-3s_BK66XMHzxaTHD5ye-nProMU",
        "AIzaSyC7FCbIc7fh5wY4SvxjQlEUCGzP7h1hr3Y",
        "AIzaSyBei_kxrqeVV200i66b7ebWa8N0RMvYzhs",
        "AIzaSyCsBmdATgysDB4g2-dqukRDWQH2vntg6lo",
        "AIzaSyDfs4swr30oBO0vbnYhFXK8d9lHX0s3c1w",
        "AIzaSyBUSdWi_Yyi1KPgJsSzGjWLELqDSYQ5t0E",
        "AIzaSyBw5zV0rNQQwR8179pgGXdkWy181RBryCc",
        "AIzaSyBIMiTr0StX9Rie4e81ckitPjQquXHdYwk",
        "AIzaSyDVHCkTrS4flwaiy1FYdz-LnRF2B3qIXGE",
        "AIzaSyCQH5wJMq2T8iePN-6QycT2fF1S29YGPn8",
        "AIzaSyDsz9QoVqVW_8JQx7DvOyU71ir2lo750Gk",
        "AIzaSyDGYjS-zWnct0ueYhXW5iFzxSRnSNeYmUg",
        "AIzaSyCG8OzN1DVznjxFJ8QM8-Ygzs8wO5yKyf8",
        "AIzaSyBtQBWRvLaOtLoYMLg3R-IeiU-27pUFKKU",
    ]
    random.shuffle(key_pool)
    key_number = len(key_pool)
    cur = 0
    while True:
        yield key_pool[cur]
        cur = (cur + 1) % key_number


if __name__ == '__main__':
    place_id_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    read_from_raw = False
    df = pandas.read_csv(r'./stops_latlon_placeid.csv')

    def get_location_name(row):
        name_array = []
        if not pandas.isnull(row['ROAD']):
            name_array.append(row['ROAD'])
        if not pandas.isnull(row['SUFFIX']):
            name_array.append(row['SUFFIX'])
        if not pandas.isnull(row['STOPNAME']):
            name_array.append(row['STOPNAME'])
        return " ".join(name_array)

    def make_text_query(index, row, key):
        global place_id_api, df
        name = get_location_name(row)
        parameters = {
            "key": key,
            'query': name,
            "location": str(row['lat']) + ',' + str(row['lon']),
            "language": "en",
            "type": "bus_station",
        }
        query_string = urllib.parse.urlencode(parameters)
        cur_url = place_id_api + '?' + query_string
        with urllib.request.urlopen(cur_url) as remote:
            result = remote.read().decode('utf-8').replace("\n", " ")
            # df.set_value(index, 'placeid_json', result)
            df.ix[index, 'placeid_json'] = result
            status = json.loads(result)['status']
            # df.set_value(index, 'status', status)
            df.ix[index, 'status'] = status
        print(status, name)
        return status, name

    keys = pick_key()
    key = next(keys)
    last_save = datetime.now().timestamp()
    total_rows = 15783
    cur_row = 0
    for index, row in df.iterrows():
        if (not pandas.isnull(row['lat'])) and (not pandas.isnull(row['lon'])) and (pandas.isnull(row['status'])):
            # keep sending query while over daily limit
            status, name = make_text_query(index, row, key)
            while status == "OVER_QUERY_LIMIT":
                time.sleep(0.5)
                key = next(keys)
                status, name = make_text_query(index, row, key)
            # save to csv file every 100 seconds:
            current_time = datetime.now().timestamp()
            if current_time - last_save > 60:
                df.to_csv('./stops_latlon_placeid.csv', index=False)
                last_save = current_time
                print("Saving at " + str(datetime.now()) +
                      ", " + str(cur_row) + "/" + str(total_rows))
        cur_row += 1
    df.to_csv('./stops_latlon_placeid.csv', index=False)
