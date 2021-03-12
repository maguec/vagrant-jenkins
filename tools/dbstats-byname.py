#!/usr/bin/env python3

import argparse
import requests
import sys
import urllib3
import json
import csv


urllib3.disable_warnings()

timeout = 10
verifyssl = False
headers_sent = {'Content-Type': 'application/json'}


parser = argparse.ArgumentParser()
parser.add_argument("--redis-host", action='store', type=str, required=True,  help="FQDN of the redis enterprise cluster")
parser.add_argument("--username", action='store', type=str, required=True,  help="Cluster Username")
parser.add_argument("--password", action='store', type=str, required=True,  help="Cluster Password")
parser.add_argument("--db-name", action='store', type=str, required=True,  help="New database name")
args = parser.parse_args()

auth=(args.username, args.password)
baseurl='https://{}:9443/'.format(args.redis_host)


j = requests.get(baseurl+"/v1/bdbs", auth=auth, headers=headers_sent, timeout=timeout, verify=verifyssl)
if j.status_code != 200:
    print('Unable to fetch db information. Status code:{} message:{}'.format(j.status_code, j.content))
    sys.exit(1)

info=j.json()
db_names = dict(map(lambda x: (x['name'], x['uid']), info))


if args.db_name not in db_names.keys():
    print('Database {} does not exist'.format(args.db_name))
    sys.exit(0)

stats_url='{}v1/bdbs/stats/{}'.format(baseurl, db_names[args.db_name])
x = requests.get(
    stats_url,
    auth=auth,
    headers=headers_sent,
    timeout=timeout,
    verify=verifyssl,
    params={'interval': '1sec'}
    )
if x.status_code == 200:
    data_file = open('data_file.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for line in x.json()['intervals']:
        if count == 0:
            header = line.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(line.values())
    data_file.close()
    sys.exit(0)
else:
    print("Unknown error while trying to grab database stats")
    x.json()
    sys.exit(1)