

1.基础环境介绍;

   软件版本信息  |系统/内核信息 |项目目录功能介绍
  -|-|-
  Python3.6     |Centos 7.2 | tools 数据库相关配置和ansible 动态主机
  Flask1.0.2    |3.10.0-862.6.3.el7.x86_64  |boot.py flask 程序启动入口文件
  Ansible2.7.7  |           | ansibleManage ansibleApi核心管理功能模块
  MYSQL5.6.0    |           |    


2.项目系统依赖包安装;
  (1).centos 7x系统安装支持包;  
  
   yum -y install python36 mysql-devel libxml2* mysql initscripts python36-devel python36-pip python36-setuptools mysql-devel libxml2*      mysql initscripts psmisc  
   
   
   (2).安装项目依赖包pip方式;  
   
   /usr/local/bin/pip3.6 install --upgrade pip  
   /usr/local/bin/pip3.6 install --upgrade setuptools  
   /usr/local/bin/pip3.6 install requests  
   /usr/local/bin/pip3.6 install Jinja2==2.10  
   /usr/local/bin/pip3.6 install flask-sqlalchemy  
   /usr/local/bin/pip3.6 install ansible  
   /usr/local/bin/pip3.6 install PyMySQL==0.9.3  
   /usr/local/bin/pip3.6 install gevent  
   /usr/local/bin/pip3.6/flask==1.0.2  
    /usr/local/bin/pip3.6/request==1.0.2  
    /usr/local/bin/pip3.6/Jinja2==2.10  
    /usr/local/bin/pip3.6/Flask-Cors==3.0.6  
    /usr/local/bin/pip3.6/flask-sqlalchemy  
    /usr/local/bin/pip3.6/flask_restful  
    /usr/local/bin/pip3.6/jsonify  
    /usr/local/bin/pip3.6/ansible  
    /usr/local/bin/pip3.6/MySQL-python    
    
3.接口文档介绍;
  
  
4.数据流走向图;
![项目数据流走向](https://github.com/breaklinux/devops-bmc-api/blob/master/img/devops-bmc-api.jpg)
    
