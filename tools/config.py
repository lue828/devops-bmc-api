"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
import os
ENVS = "dev,test,testone,ontest,prod"
class MysqlConfig(object):
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "123456"
    HOST = "192.168.1.1"
    PORT = "3306"
    DATABASE = "op_bmc"
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
