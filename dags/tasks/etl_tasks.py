# -*- coding: utf-8 -*-

import glob as gl
import os
import logging
import json
import requests
from datetime import datetime
from airflow.hooks.mysql_hook import MySqlHook
from math import ceil

def read_and_store_files(**context):
    logging.info('Reading Input Files')
    files = gl.glob('./dags/data/*')
    connection = MySqlHook(mysql_conn_id='airflow_db')

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
                column_request = ['uri', 'url', 'size', 'querystring']
                column_response = ['status','size']
                column_consumer = ['uuid']
                column_service = ['connect_timeout','created_at','host', 'id', 'name', 'path', 'port', 'protocol', 'read_timeout', 'retries', 'updated_at', 'write_timeout']
                column_route = ['created_at','hosts','id', 'methods', 'paths', 'preserve_host', 'protocols', 'regex_priority', 'strip_path', 'updated_at']
                column_latencies = ['proxy', 'kong', 'request']
                column_process = []

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
                        request.append(line["request"][attribute])

                # response attribute
                for attribute in line["response"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_response) 
                    if res == True:
                        response.append(line["response"][attribute])

                # consumer attribute
                for attribute in line["authenticated_entity"]["consumer_id"]:
                    if attribute == 'uuid':
                        consumer.append(line["authenticated_entity"]["consumer_id"][attribute])

                # service attribute
                for attribute in line["service"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_service) 
                    if res == True:
                        service.append(line["service"][attribute])

                # route attribute
                for attribute in line["route"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_route) 
                    if res == True:
                        route.append(line["route"][attribute])

                # latencies attribute
                for attribute in line["latencies"]:
                    newatt = attribute.lower().replace('-', '_')
                    res = any(att in newatt for att in column_latencies) 
                    if res == True:
                        latencies.append(line["latencies"][attribute])

                logging.info(column_headers)
                logging.info(headers)

                id = connection.insert_row(
                    table='headers',
                    rows=headers,
                    replace=True
                )

                logging.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAIIIIID" + str(id))
                logging.info(str(count) + ' records saved')

    return None
