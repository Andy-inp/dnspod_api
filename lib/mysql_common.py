#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_config import get_config
from models.dnspod_models import *
from conf.get_mylogger import mylogger



class Mysql_common(object):

    config_data = get_config('mysql')
    _m_database = config_data['db']
    _m_user = config_data['user']
    _m_passwd = config_data['password']
    _m_ip = config_data['ip']
    _m_port = config_data['port']

    def __init__(self):
        self._engine = create_engine(f"mysql+pymysql://{self._m_user}:{self._m_passwd}@{self._m_ip}:{self._m_port}/{self._m_database}", max_overflow=5)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()


    def insert(self, table_class, table_data):
        try:
            insertdata = table_class(**table_data)
            self._session.add(insertdata)
            self._session.commit()
            print(f"\033[32m数据入库成功，入库数据{table_data}\033[0m")
        except Exception as e:
            print("\033[31m数据入库失败!!!检查日志：logs/operate.log\033[0m")
            mylogger.error(f"插入数据失败，失败原因：{e.__str__()}")


    def delete(self, table_class, table_data):
        pass


    def update(self):
        pass


    def get(self, table_class, condition=None):
        try:
            result = self._session.query(table_class).all()
            if condition:
                res = result
            else:
                res = result
                return res
        except Exception as e:
            print("\033[31m查询数据失败!!!检查日志：logs/operate.log\033[0m")
            mylogger.error(f"查询数据失败，失败原因：{e.__str__()}")



# if __name__ == '__main__':
#     m = Mysql_common()
#     # for i in m.get(Record_List):
#     #     print(i)
#     # for e in m.get(Domain_List):
#     #     print(e)
#     # insert_data = {'domain_id': 111, 'status': 'enable', 'ttl': '600', 'domain_name': 'testaaa.com'}
#     # m.insert(Domain_List, insert_data)
# 
# 
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from lib.dnspod_api import *
#     from models.dnspod_models import Domain_List, Record_List
#     from bin.start import MyThread
#     import time
#     from queue import Queue
#     import threading
# 
#     login_token = 'you_login_token'
#     domain_api_instance = Dnspod_Api_Domain(login_token)
#     record_api_instance = Dnspod_Api_Record(login_token)
#     insert_data = {}
#     thread_list = []
# 
#     # domain_list
#     # domain_info = domain_api_instance.get_domain_list()
#     # for data in domain_info['data']['domains']:
#     #     insert_data['domain_id'] = data['id']
#     #     insert_data['status'] = data['status']
#     #     insert_data['ttl'] = data['ttl']
#     #     insert_data['domain_name'] = data['name']
#     #     insert_data['owner'] = data['owner']
#     #     insert_data['records_amount'] = data['records']
#     #     m.insert(Domain_List, insert_data)
# 
# 
#     # record_list
#     class Second_Getmysql(Domain_List):
#         def __repr__(self):
#             return f"{self.domain_name}"
# 
#     class Second_Thread(MyThread):
#         def run(self):
#             self.result = self.func(*self.args)
# 
# 
# 
#     class ThreadPoolManger():
#         """线程池管理器"""
#         def __init__(self, thread_num):
#             # 初始化参数
#             self.work_queue = Queue()
#             self.thread_num = thread_num
#             self.__init_threading_pool(self.thread_num)
#     
#         def __init_threading_pool(self, thread_num):
#             # 初始化线程池，创建指定数量的线程池
#             for i in range(thread_num):
#                 self.thread = MyThread(self.work_queue)
#                 self.thread.start()
#     
#         def add_job(self, func, *args):
#             # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
#             self.work_queue.put((func, args))
#             return self.thread
#     
#     class MyThread(threading.Thread):
#         """定义线程类，继承threading.Thread"""
#         def __init__(self, work_queue):
#             super(MyThread, self).__init__()
#             self.work_queue = work_queue
#             #self.daemon = True
#     
#         def run(self):
#             # 启动线程
#             while True:
#                 target, args = self.work_queue.get()
#                 result = target(*args)
# 
#                 try:
#                     record_list = result['data']['records']
#                     for record_result in record_list:
#                         insert_data['record_id'] = record_result['id']
#                         insert_data['sub_domain'] = record_result['name']
#                         insert_data['record_line'] = record_result['line']
#                         insert_data['record_type'] = record_result['type']
#                         insert_data['ttl'] = record_result['ttl']
#                         insert_data['value'] = record_result['value']
#                         insert_data['status'] = record_result['status']
#                         insert_data['belong_domain'] = result['data']['belong_domain']
#                         m.insert(Record_List, insert_data)
#                 except KeyError:
#                    record_error_domain = result['domain']
#                    print(f"域名{record_error_domain}获取数据失败!")
#                    mylogger.error(f"域名{record_error_domain}获取数据失败!")
# 
#                 self.work_queue.task_done()
# 
# 
#     thread_pool = ThreadPoolManger(1)
# 
#     domains = m.get(Second_Getmysql)
#     for d in domains:
#         thread_pool.add_job(record_api_instance.get_record_list, str(d))
# 
# 
# 


#     domains = m.get(Second_Getmysql)
# 
#     for d in domains:
#         record_thread = Second_Thread(record_api_instance.get_record_list, args=(str(d),))
#         thread_list.append(record_thread)
#         record_thread.start()
#     for t in thread_list:
#         t.join()
#         record_list = t.get_result()
# 
#         try:
#             record_list2 = record_list['data']['records']
#             for record_result in record_list2:
#                     insert_data['record_id'] = record_result['id']
#                     insert_data['sub_domain'] = record_result['name']
#                     insert_data['record_line'] = record_result['line']
#                     insert_data['record_type'] = record_result['type']
#                     insert_data['ttl'] = record_result['ttl']
#                     insert_data['value'] = record_result['value']
#                     insert_data['status'] = record_result['status']
#                     insert_data['belong_domain'] = record_list['data']['belong_domain']
#                     print(insert_data)
#                     #m.insert(Record_List, insert_data)
#         except KeyError as e:
#             record_error_domain = record_list['domain']
#             print(f"域名{record_error_domain}获取数据失败!")
#             mylogger.error(f"域名{record_error_domain}获取数据失败!")
# 
# 
# 
