from flask import Blueprint, request,jsonify
import json
import plotly
import plotly.graph_objs as go
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

from flaskr.yxl.es import Baidu_hotnews

bp = Blueprint('baidu', __name__, url_prefix='/baidu')

op = Baidu_hotnews()
@bp.route('/search')
def search():
    offset = request.args['offset']
    limit = request.args['limit']
    hotname = request.args['hotname']
    region = request.args['region']
    result = {}
    if hotname !='' and region != '':
        result = op.search_by_condition(hotname, region)
    else:
        result = op.search(offset, limit)
    hits = result['hits']
    total = result['total']
    data = []
    for item in hits:
        source = item['_source']
        source['ID'] = item['_id']
        data.append(source)
    #print(data)
    return jsonify({'total': total, 'rows': data})

@bp.route('/graph')
def draw():
    result = op.aggs_pubtime_30day()
    df = json_normalize(result) # creating a sample dataframe
    df.sort_values(by="key",ascending=True,inplace=True)
    #print(df)
    df['key'] = df['key'].apply(lambda x: str(x[4:6] + '月' + x[6:]) + '日')
    data = [
        # go.Scatter(
        #     x=df['key'], # assign x as the dataframe column 'x'
        #     y=df['doc_count'],
        #     mode = 'lines',#散点图
        #     name ='lines',#设置散点的名字，但单个图像不起作用
        #     marker = dict(
        #         size =5,#设置点的宽度
        #         color = 'rgba(100,149,237, .8)'#设置点的颜色，这个可以根据网上对照更改颜色
        #     )
        # ),
         go.Bar(
            x=df['key'], # assign x as the dataframe column 'x'
            y=df['doc_count'],
            name = 'bars',
            marker=dict(
                color = '#4682B4' #设置条形图的颜色
            ),
            opacity=0.9   #条形图颜色的不透明度
        )    
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@bp.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        ids = ""
        for item in json_data:
            id = item['ID']
            if ids == "":
                ids = id
            else:
                ids = ids + ',' + id
        print(ids)
        result = op.delete_bulk_ids(ids)
        print(result)
        response = {}
        if len(result['failures']) == 0:
            response['errorCode'] = 200
        else:
             response['errorCode'] = 500
        return jsonify(response)

@bp.route('/demo')
def demo():
    data = '''
    [
      {
          "GUID": "c21da9601e152096d627737444371b35",
          "HOT_NAME": "男子为偷长城砖被困",
          "HOT_NUM": 15,
          "REGION": "澳门",
          "LOAD_TIME": "2019/12/29 15:51:55"
      },
      {
          "GUID": "993a807577a9b5dab35c472c79a93a78",
          "HOT_NAME": "2019年5年房贷利率",
          "HOT_NUM": 30,
          "REGION": "澳门",
          "LOAD_TIME": "2019/12/29 15:51:55"
      },
      {
          "GUID": "cdb5056d7641d78d6af026b03509f12a",
          "HOT_NAME": "男子为偷长城砖被困",
          "HOT_NUM": 15,
          "REGION": "澳门",
          "LOAD_TIME": "2019/12/29 15:41:55"
      }
    ]
    '''
    return data