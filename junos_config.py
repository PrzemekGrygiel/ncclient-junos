#!/usr/bin/env python

import argparse
from ncclient import manager
from ncclient.xml_ import *
import time


def connect(host, port, user, password):
    return  manager.connect(host=host, port=port,username=user,password=password,hostkey_verify=False,timeout=30,device_params={'name': 'junos'})


def create_config(fxp0_ip,filename):
    with open(filename) as f:
        configuration = f.readlines()
    print configuration
    return configuration

def setup_junos(conf, fxp0_ip):
    with connect(host=fxp0_ip, port="22", user="root", password="c0ntrail123") as m:
        m.lock()
        print conf
        send_config = m.load_configuration(action='set', config=conf)
        print send_config.tostring
        commit_config = m.commit(timeout='30')
        print commit_config.tostring
        m.unlock()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        usage="python junos_config.py --fxp0-ip 192.168.111.9 --filename config.txt")
    parser.add_argument(
        '--fxp0-ip',
        required=True
    )
    parser.add_argument(
        '--filename',
        required=True
    )
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(2)
    parsed_params, _ = parser.parse_known_args(sys.argv[1:])
    print  parsed_params.fxp0_ip
    config = create_config( parsed_params.fxp0_ip, parsed_params.filename)
    setup_junos(config, parsed_params.fxp0_ip)
