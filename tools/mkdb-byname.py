#!/usr/bin/env python3

import argparse
import requests
import sys
import urllib3
import json


urllib3.disable_warnings()

timeout = 10
verifyssl = False
headers_sent = {'Content-Type': 'application/json'}


parser = argparse.ArgumentParser()
parser.add_argument("--redis-host", action='store', type=str, required=True,  help="FQDN of the redis enterprise cluster")
parser.add_argument("--username", action='store', type=str, required=True,  help="Cluster Username")
parser.add_argument("--password", action='store', type=str, required=True,  help="Cluster Password")
parser.add_argument("--db-name", action='store', type=str, required=True,  help="New database name")
parser.add_argument("--memory-size", action='store', type=int, required=True,  help="Size of DB in bytes")
parser.add_argument("--db-password", action='store', type=str, help="New database name")
parser.add_argument("--shard-count", action='store', type=int, default=1, help="Number of DB shards")
parser.add_argument("--db-port", action='store', type=int, help="Port to use for the database")
parser.add_argument("--replication", action='store_true', help="Enable database repliction")
args = parser.parse_args()

auth=(args.username, args.password)
baseurl='https://{}:9443/'.format(args.redis_host)


j = requests.get(baseurl+"/v1/bdbs", auth=auth, headers=headers_sent, timeout=timeout, verify=verifyssl)
if j.status_code != 200:
    print('Unable to fetch db information. Status code:{} message:{}'.format(j.status_code, j.content))
    sys.exit(1)

info=j.json()
db_names = list(map(lambda x: x['name'], info))

if args.db_name in db_names:
    print('Database {} already exists'.format(args.db_name))
    sys.exit(0)

db_settings = {
    'name': args.db_name,
    'memory_size': args.memory_size,
    'shards_count': args.shard_count,
}

if args.db_password:
    db_settings['authentication_redis_pass'] = args.db_password

if args.shard_count > 1:
    db_settings['sharding'] = True
else:
    db_settings['sharding'] = False

if args.db_port:
    db_settings['port'] = args.db_port

if args.replication:
    db_settings['replication'] = args.replication
else:
    db_settings['sharding'] = False


print(db_settings)

x= requests.post(baseurl+"/v1/bdbs", auth=auth, headers=headers_sent, timeout=timeout, verify=verifyssl, json=db_settings)
if x.status_code != 200:
    print("Error Creating database: " )
    print(x.content)
    sys.exit(1)

print('Databse {} sucessfully created'.format(args.db_name))