import json

from flask import Flask, request, Response, Blueprint
from SQLinjection.hander.hd_base import require
from SQLinjection.sql import errorsql

bp = Blueprint('error', __name__, url_prefix='/error')


@bp.route('/GetDBName', methods=['POST'])
@require('url')
def GetDBName():
    DBName = errorsql.GetDBName(request.json.get('url'))
    t = {"code": 0,
         "message": "爆破成功",
         "DBName": DBName
         }
    return Response(json.dumps(t), mimetype='application/json')


@bp.route('/GetDBTables', methods=['POST'])
@require('url', "DBName")
def GetDBTables():
    DBTables = errorsql.GetDBTables(request.json.get('url'), request.json.get('DBName'))
    listID = range(1, len(DBTables) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBTables": dict(zip(listID, DBTables))
         }
    return Response(json.dumps(t), mimetype='application/json')


@bp.route('/GetDBColumns', methods=['POST'])
@require('url', "DBName", "DBTable")
def GetDBColumns():
    DBColumns = errorsql.GetDBColumns(request.json.get('url'), request.json.get('DBName'), request.json.get('DBTable'))
    listID = range(1, len(DBColumns) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBColumns": dict(zip(listID, DBColumns))
         }
    return Response(json.dumps(t), mimetype='application/json')


@bp.route('/GetDBData', methods=['POST'])
@require('url', "DBName", "DBTable", "DBColumn")
def GetDBData():
    DBData = errorsql.GetDBData(request.json.get('url'), request.json.get('DBName'), request.json.get('DBTable'),
                                request.json.get('DBColumn'))
    listID = range(1, len(DBData) + 1)
    t = {"code": 0,
         "message": "爆破成功",
         "DBData": DBData
         }
    return Response(json.dumps(t), mimetype='application/json')
