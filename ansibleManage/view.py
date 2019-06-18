"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from flask import Blueprint
from flask import request, Response
from ansibleManage.ansibleApi import AnsibleApi

import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "tools")
os.sys.path.append(script_path)
from tools.ansibleInventory import HostApi

ansibleUrl = Blueprint('ansible', __name__)


@ansibleUrl.route('/api/v1', methods=['GET', 'POST'])
def ansibleRun():
    import json
    from tools.bmc_log import bmcLogInster
    from ansibleManage.ansibleApi import AnsibleApi
    if request.method == "GET":
        return ansibleSelect()
    elif request.method == "POST":
        Data = request.get_json()
        inenory_ip = Data.get('instance_ip', None)
        command = Data.get('command', None)
        args = Data.get('args', None)
        becomeUser = Data.get("user", "root")
        data = {"code": 1, "message": "instance_ip or command error"}
        if inenory_ip:
            t = HostApi()
            Ansible_run = AnsibleApi(script_path + "/static_hosts", "ops", becomeUser)
            Ansible_run.run(inenory_ip, command, args)
            reults = Ansible_run.get_result()
            if command == "shell":
                reults = ansibleCallbackFilter(reults)

            if ansibleInsert(inenory_ip, command, args, json.dumps(reults)):
                print("成功")
            else:
                print("失败")
            bmcLogInster("ansibleRun", request, reults)
            data = {"code": 0, "data": reults, "message": "success"}
        return Response(json.dumps(data), mimetype='application/json')
    elif request.method == "DELETE":
        pass

    else:
        parameterInfo = "参数错误,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


@ansibleUrl.route('/module/v1', methods=['GET', 'POST'])
def ansibleModule():
    instanceModule = ansibelBase()
    data = instanceModule.Ansible_module()
    return Response(data, mimetype='application/json')


def ansibleInsert(ip, command, args, callback):
    from models import db
    from models import bmc_ansible
    try:
        ansibleDataInsert = bmc_ansible(run_ip=ip, command_name=command, run_agrs=args, ansible_callback=callback)
        db.session.add(ansibleDataInsert)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def ansibleSelect():
    import json
    from models import bmc_ansible
    queryData = bmc_ansible.query.all()
    return Response(json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in queryData]}),
                    mimetype='application/json')


def ansibleCallbackFilter(callback):
    callbackData = dict()
    for i in callback:
        callbackData[i] = list()
        for x in callback[i]:
            if isinstance(callback[i][x], dict):
                callbackData[i].append({x: {"status": callback[i][x]["changed"],
                                            "messages": callback[i][x]["stdout"] or callback[i][x]["stderr"]}})
            else:
                callbackData[i].append({x: {"status": True, "messages": callback[i][x]}})
    return callbackData


class ansibelBase(object):
    def Ansible_module(self):
        import json
        Commands_list = ["shell", "command", "script", "telnet", "raw", "expect", "psexec"]
        File_list = ["copy", "fetch", "find", "stat", "file", "synchronize", "patch"]
        Pckaging_list = ["yum", "yum_repository ", "maven", "npm", "gem", "pip", "bundler"]
        Service_list = ["service"]
        return json.dumps({"code": 0, "data": dict(Command=Commands_list, File=File_list, Package=Pckaging_list,
                                                   Service=Service_list)})


@ansibleUrl.route('/host/v1', methods=['GET', 'POST'])
def ansibleHostRun():
    try:
        if request.method == "GET":
            return ansibleHostSelect()
        elif request.method == "POST":
            return ansibleInsterHost()
        elif request.method == "DELETE":
            pass
        else:
            data = "方法不存在"
            return data
    except Exception as e:
        print(e)


def ansibleHostSelect():
    import json
    from models import bmc_ansible_hosts
    queryData = bmc_ansible_hosts.query.all()
    return Response(
        json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in queryData]}, ),
        mimetype='application/json')


def ansibleInsterHost():
    import json
    from flask import Response
    from models import db
    from models import bmc_ansible_hosts
    import datetime
    Data = request.get_json()
    host_ip = Data.get('instanceip', None)
    username = Data.get('username', None)
    password = Data.get('password', None)
    port = Data.get('port', None)
    group = Data.get("group")
    create_time = datetime.datetime.now()
    try:
        if host_ip and group and port and username and password:
            ip = host_ip.split(',');
            for i in ip:
                ansibleHostDataInsert = bmc_ansible_hosts(host=i, username=username, password=password, port=port,
                                                          group=group, createtime=create_time)
                db.session.add(ansibleHostDataInsert)
                db.session.commit()
            msg = "Insert Success"
            return Response(json.dumps({"code": 0, "data": msg}), mimetype='application/json')
        else:
            data = "参数缺少,不允许添加"
            return Response(json.dumps({"code": 1, "data": data}), mimetype='application/json')
    except Exception  as e:
        print(e)
        return Response(json.dumps({"code": 1, "data": "error"}), mimetype='application/json')
