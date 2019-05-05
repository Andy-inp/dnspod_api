#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_config import get_config, Base_Dir
from lib.dnspod_api import *
from lib.mysql_common import Mysql_common
from lib.get_atm_data import Atm_Data
from conf.get_mylogger import mylogger
from models.dnspod_models import Domain_List, Record_List


# 清空线程列表
thread_list = []
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None



def menu(choose, others_info=None):
    '''Menu'''

    # Add Domain
    if choose == 1:

        for d in domains:
            domain_thread = MyThread(domain_api_instance.add_domain, args=(d,))
            thread_list.append(domain_thread)
            domain_thread.start()
        for t in thread_list:
            t.join()
            return_data = t.get_result()
            if return_data['status'] == 'success':
                print(f"\033[32m域名{return_data['data']['domain_name']}添加成功，并存入DB \033[0m")
                mylogger.info(f"域名{return_data['data']['domain_name']}添加成功")
                mysql_instance.insert(Domain_List,return_data['data'])
            else:
                print(f"\033[31m域名{return_data['data']['domain_name']}添加失败，失败原因：{return_data['message']}，错误代码：{return_data['data']['code']}\033[0m")
                mylogger.error(f"域名{return_data['data']['domain_name']}添加失败, 失败原因：{return_data['message']}，错误代码：{return_data['data']['code']}")
        sys.exit(1)


    # Add Record
    elif choose == 2:

        record_sub = input('请输入记录主机头：')
        record_type = input('请输入记录类型：')
        record_line = input('请输入记录线路(默认|国内|国外 等)：')
        record_value = input('请输入记录值：')

        for d in domains:
            record_thread = MyThread(record_api_instance.add_record, args=(d, record_sub, record_type, record_line, record_value))
            thread_list.append(record_thread)
            record_thread.start()
        for t in thread_list:
            t.join()
            return_data = t.get_result()
            if return_data['status'] == 'success':
                print(f"\033[32m域名{return_data['data']['belong_domain']}添加主机头{return_data['data']['sub_domain']}到记录{return_data['data']['value']}成功，并存入DB \033[0m")
                mylogger.info(f"域名{return_data['data']['belong_domain']}添加主机头{return_data['data']['sub_domain']}到记录{return_data['data']['value']}成功")
                mysql_instance.insert(Record_List,return_data['data'])
            else:
                print(f"\033[31m域名{return_data['data']['belong_domain']}添加主机头{return_data['data']['sub_domain']}失败，失败原因：{return_data['message']}，错误代码：{return_data['data']['code']}\033[0m")
                mylogger.error(f"域名{return_data['data']['belong_domain']}添加主机头{return_data['data']['sub_domain']}失败，失败原因：{return_data['message']}，错误代码：{return_data['data']['code']}")
        sys.exit(1)


    # Select database
    elif choose == 3:
        sys.exit(1)


    else:
        sys.exit(0)



if __name__ == '__main__':

    # select token and others_info
    token_data = get_config('dnspod_api_token')
    others_data = get_config('others_info')

    select_product = sys.argv[1]
    if select_product == 'you_logintoken':
        login_token = token_data['you_logintoken']
        others_info = others_data['test1']
    else:
        print('''
        未找到对应产品，请检查!
        用法：
            python start.py xxx
        所有产品信息位于config.yml文件中
        ''')
        sys.exit(0)

    # domain.txt
    domain_init = input(f"\033[33m请输入要操作的域名(已,为分隔符),留空则从文件 {Base_Dir}/bin/domain.txt 读入域名：\033[0m")
    with open(f"{Base_Dir}/bin/domain.txt", 'r') as f:
        domains = domain_init.split(',') if domain_init else f.read().splitlines()

    # instance 
    domain_api_instance = Dnspod_Api_Domain(login_token)
    record_api_instance = Dnspod_Api_Record(login_token)
    atm_data_instance = Atm_Data()
    mysql_instance = Mysql_common()


    while True:
        choose = int(input("\n\n\t\t \033[4m功能说明\033[0m\n\n"
                       "\t\033[34m1\033[0m \t添加域名\n"
                       "\t\033[34m2\033[0m \t添加记录\n"
                       "\t\033[34m3\033[0m \t查询功能(域名和记录列表)\n"
                       "\t\033[34m4\033[0m \t退出\n\n"
                       "\033[33m请输入您要操作任务的序号：\033[0m"))

        menu(choose, others_info)


