import logging

def query(cursor, db, count, headers, request, response, consumer, service, route, latencies, process, column_headers, column_request, column_response, column_consumer, column_service, column_route, column_latencies, column_process):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # headers table
        columns = ", ".join(column_headers)
        data = "', '".join(headers)
        sql = "INSERT INTO headers (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        header_id = db.insert_id()

        # append header key to request and response
        request.append(str(header_id))
        response.append(str(header_id))

        # requests table
        columns = ", ".join(column_request)
        data = "', '".join(request)
        sql = "INSERT INTO requests (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        request_id = db.insert_id()

        # response table
        columns = ", ".join(column_response)
        data = "', '".join(response)
        sql = "INSERT INTO response (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        response_id = db.insert_id()

        # consumer table
        columns = ", ".join(column_consumer)
        data = "', '".join(consumer)
        sql = "INSERT INTO consumer (id) values (' " + data + " ');"
        cursor.execute(sql)
        consumer_id = db.insert_id()

        # latencies table
        columns = ", ".join(column_latencies)
        data = "', '".join(latencies)
        sql = "INSERT INTO latencies (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        latencies_id = db.insert_id()

        # services table
        columns = ", ".join(column_service)
        data = "', '".join(service)
        sql = "INSERT INTO services (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        services_id = db.insert_id()

        # append service_id key to route
        route.append(str(services_id))

        # routes table
        columns = ", ".join(column_route)
        data = "', '".join(route)
        sql = "INSERT INTO routes (" + columns + ") values (' " + data + " ');"
        cursor.execute(sql)
        services_id = db.insert_id()

        db.commit()

        logging.info(str(count) + ' records saved')
    except:
        logging.info('Error on record ' + str(count))