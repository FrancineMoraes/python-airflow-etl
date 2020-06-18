# -*- coding: utf-8 -*-

import glob as gl
import os
import logging
import json
import MySQLdb as mysqldb
from airflow.hooks.mysql_hook import MySqlHook
from sqlalchemy import create_engine
import pandas as pd
from math import ceil
from tasks import query

def read_and_store_files(**context):
    logging.info('Reading Input Files')
    files = gl.glob('./dags/data/*')

    db = mysqldb.connect("172.19.0.3","root","password","me_etl")
    cursor = db.cursor()

    entries = []

    for f in files:
        count = 0

        with open(f) as opened_file:
            logging.info('Opening File' + f)

            while True:
                count += 1

                headers = []
                request = []
                response = []
                consumer = []
                service = []
                route = []
                latencies = []
                process = []

                column_headers = ['content_length', 'via', 'connection', 'access_control_allow_credentials', 'content_type', 'server', 'access_control_allow_origin', 'accept', 'host', 'user_agent']
                column_request = ['method', 'uri', 'url', 'size', 'querystring', 'headers_id']
                column_response = ['status','size', 'headers_id']
                column_consumer = ['uuid']
                column_service = ['connect_timeout','created_at','host', 'id', 'name', 'path', 'port', 'protocol', 'read_timeout', 'retries', 'updated_at', 'write_timeout']
                column_route = ['created_at','hosts','id', 'methods', 'paths', 'preserve_host', 'protocols', 'regex_priority', 'strip_path', 'updated_at', 'services_id']
                column_latencies = ['proxy', 'kong', 'request']
                column_process = ['upstream_uri_id', 'client_ip', 'started_at']

                line = opened_file.readline().split()

                if not line:
                    break

                line = json.loads(line[0])

                # response headers attributes
                for attribute in line["response"]["headers"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_headers) 
                    if res == True:
                        headers.append(str(line["response"]["headers"][attribute]))

                # request headers attributes
                for attribute in line["request"]["headers"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_headers) 
                    if res == True:
                        headers.append(str(line["request"]["headers"][attribute]))

                # save headers and return id to attribute on request and response

                # request attribute
                for attribute in line["request"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_request) 
                    if res == True:
                        request.append(str(line["request"][attribute]))

                # response attribute
                for attribute in line["response"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_response) 
                    if res == True:
                        response.append(str(line["response"][attribute]))

                # consumer attribute
                for attribute in line["authenticated_entity"]["consumer_id"]:
                    if attribute == 'uuid':
                        consumer.append(str(line["authenticated_entity"]["consumer_id"][attribute]))

                # service attribute
                for attribute in line["service"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_service) 
                    if res == True:
                        service.append(str(line["service"][attribute]))

                # route attribute
                for attribute in line["route"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_route) 
                    if res == True:
                        route.append(str(line["route"][attribute]).replace("'", ""))

                # latencies attribute
                for attribute in line["latencies"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_latencies) 
                    if res == True:
                        latencies.append(str(line["latencies"][attribute]))

                query.query(cursor, db, count, headers, request, response, consumer, service, route, latencies, process, column_headers, column_request, column_response, column_consumer, column_service, column_route, column_latencies, column_process)
    return None
