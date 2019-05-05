#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()



class Domain_List(Base):
    __tablename__ = 'domain_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column(Integer, unique=True, nullable=True)
    status = Column(String(64))
    ttl = Column(String(32))
    domain_name = Column(String(128), unique=True, nullable=True)
    owner = Column(String(128))
    records_amount = Column(Integer)

    def __repr__(self):
        return f"domain_id: {self.domain_id}, status: {self.status}, domain_name: {self.domain_name}"



class Record_List(Base):
    __tablename__ = 'record_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, unique=True, nullable=True)
    sub_domain = Column(String(128), nullable=True)
    record_line = Column(String(32))
    record_type = Column(String(32))
    ttl = Column(Integer)
    value = Column(String(128), nullable=True)
    status = Column(String(32))
    belong_domain = Column(String(64), ForeignKey('domain_list.domain_name'))
    
    domains = relationship('Domain_List', backref='records')

    def __repr__(self):
        return f"record_id: {self.record_id}, sub_domain: {self.sub_domain}, record_line: {self.record_line}, record_type: {self.record_type}, value: {self.value}, belong_domain: {self.belong_domain}"



if __name__ == '__main__':
    Base.metadata.create_all(engine)
