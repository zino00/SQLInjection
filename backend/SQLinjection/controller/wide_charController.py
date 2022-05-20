import json

from flask import Flask, request, Response
from SQLinjection.hander.hd_base import require
from SQLinjection.sql import wide_charsql

app = Flask(__name__)


@app.route('/wide_char/GetDBName', methods=['POST'])
@require('url')
def GetDBName():
    DBName = wide_charsql.GetDBName(request.json.get('url'))
    t = {"code": 0,
         "message": "爆破成功",
         "DBName": DBName
         }
    return Response(json.dumps(t), mimetype='application/json')


@app.route('/wide_char/GetDBTables', methods=['POST'])
@require('url', "DBName")
def GetDBTables():
    DBTables = wide_charsql.GetDBTables(request.json.get('url'), request.json.get('DBName'))
    listID = range(1, len(DBTables) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBTables": dict(zip(listID, DBTables))
         }
    return Response(json.dumps(t), mimetype='application/json')


@app.route('/wide_char/GetDBColumns', methods=['POST'])
@require('url', "DBName", "DBTable")
def GetDBColumns():
    DBColumns = wide_charsql.GetDBColumns(request.json.get('url'), request.json.get('DBName'), request.json.get('DBTable'))
    listID = range(1, len(DBColumns) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBColumns": dict(zip(listID, DBColumns))
         }
    return Response(json.dumps(t), mimetype='application/json')


@app.route('/wide_char/GetDBData', methods=['POST'])
@require('url', "DBName", "DBTable", "DBColumn")
def GetDBData():
    DBData = wide_charsql.GetDBData(request.json.get('url'), request.json.get('DBName'), request.json.get('DBTable'),
                                request.json.get('DBColumn'))
    listID = range(1, len(DBData) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBData": DBData
         }
    return Response(json.dumps(t), mimetype='application/json')


if __name__ == '__main__':
    app.run()
