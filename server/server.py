from flask import Flask, send_from_directory, Response
import pandas
import json

app = Flask(__name__, static_url_path='/web/static')

routes = pandas.read_csv('./csv/routes.csv')
users = pandas.read_csv('./csv/20090228_with_date.csv')


def get_route_from_onoff(on, off):
    cur_result = []
    result_row = routes[routes['On'] == on][routes['Off'] == off]
    if not result_row.empty:
        for index, row in result_row.iterrows():
            if row['STATUS'] == 'OK':
                cur_result.append(row['ROUTES'])
    return cur_result


@app.route('/ceed/', methods=['GET'])
def root():
    return send_from_directory('web/static', 'index.html')


@app.route('/ceed/<path:path>/', methods=['GET'])
def serve_static(path):
    # send_static_file will guess the correct MIME type
    return send_from_directory('web/static/', path)


@app.route('/ceed/cardid/<int:id>/', methods=['GET'])
def get_user_json(id):
    user_routes = []
    user_rows = users[users['CardId'] == id]
    for index, row in user_rows.iterrows():
        cur_on = row['OnLandmark']
        cur_off = row['OffLandmark']
        if not pandas.isnull(cur_on) and not pandas.isnull(cur_on):
            cur_route = get_route_from_onoff(cur_on, cur_off)
            user_routes.extend(cur_route)
    with open('./sample_res.json', 'w') as f:
        json.dump(user_routes, f, indent=2)
    print("Get %d routes for card id %d." % (len(user_routes), id))
    res = Response(response=json.dumps(user_routes),
                   status=200, mimetype='application/json')
    return res


if __name__ == "__main__":
    app.run()
