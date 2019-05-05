#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import sys, os
import yaml

Base_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config(service):
    with open(f"{Base_Dir}/conf/config.yml", 'r') as f:
        cfg = yaml.full_load(f)
        config_data = cfg[service]
        return config_data

