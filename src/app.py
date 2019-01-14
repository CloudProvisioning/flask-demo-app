from flask import Flask, render_template, jsonify
import psycopg2
import json
import random
from flask_cors import CORS
import os
from faker import Faker
import petname
import petname.english
from flask import request
import datetime
import time

app = Flask(__name__)
CORS(app)

fake = Faker()
server_id = fake.pyint()

def get_db_connection():
    dbname = os.environ['DB_NAME']
    dbuser = os.environ['DB_USER']
    dbhost = os.environ['DB_HOST']
    dbport = os.environ['DB_PORT']

    connection = psycopg2.connect(database=dbname, user=dbuser, host=dbhost, port=dbport)
    #connection = psycopg2.connect(database='cp_test_db', user='root', host='192.168.201.51', port=31691)
    
    return connection

@app.route('/')
def index():   
    return 'Hello from Flask application. Server id: ' + str(server_id)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        start_time = time.time()

        cursor = get_db_connection().cursor()
        cursor.execute("SELECT id, first_name, last_name, age, employment, location, pet_name, favorite_color, server_id, add_timestamp FROM people")
        entries = cursor.fetchall()

        raw_result = []
        for entry in entries:
            item = dict(
                id=str(entry[0]),
                firstName=entry[1],
                lastName=entry[2],
                age=entry[3],
                employment=entry[4],
                location=entry[5],
                petName=entry[6],
                favoriteColor=entry[7],
                serverId=entry[8],
                addTimestamp=entry[9]
            )
            raw_result.append(item)

        end_time = time.time()
        result = dict(
            status='success',
            message=str(len(entries)) + ' entries has loaded from database successfully',
            payload=raw_result,
            elapsed=str(datetime.timedelta(seconds=(end_time - start_time)))
        )

        return jsonify(result)

    except Exception as e:
        print(str(e))
        result = dict(
            status='failure',
            message=str(e),
            payload=None,
            elapsed='00:00:00.0'
        )
        return jsonify(result)

@app.route('/add', methods=['POST'])
def add_data():
    try:
        start_time = time.time()

        count = request.get_json()['count']
        connection = get_db_connection()
        cursor = connection.cursor()

        queue_amount = 1000
        ranges_quantity = count // queue_amount
        data_reminder = count - queue_amount * ranges_quantity

        for x in range(ranges_quantity):
            values = generate_data(queue_amount)
            sql_query = ''
            for value in values:
                subquery = "INSERT INTO people (first_name, last_name, age, employment, location, pet_name, favorite_color, server_id, add_timestamp) VALUES ('" + value.get('firstName') + "', '" + value.get('lastName') + "', " + str(value.get('age')) + ", '" + value.get('employment') + "', '" + value.get('location') + "', '" + value.get('petName') + "', '" + value.get('favoriteColor') + "', " + str(value.get('serverId')) + ", '" + value.get('addTimestamp') + "'); \n "
                sql_query += subquery
            cursor.execute(sql_query)
            connection.commit()
            sql_query = ''

        if data_reminder != 0:
            values = generate_data(data_reminder)
            sql_query = ''
            for value in values:
                subquery = "INSERT INTO people (first_name, last_name, age, employment, location, pet_name, favorite_color, server_id, add_timestamp) VALUES ('" + value.get('firstName') + "', '" + value.get('lastName') + "', " + str(value.get('age')) + ", '" + value.get('employment') + "', '" + value.get('location') + "', '" + value.get('petName') + "', '" + value.get('favoriteColor') + "', " + str(value.get('serverId')) + ", '" + value.get('addTimestamp') + "'); \n "
                sql_query += subquery
            cursor.execute(sql_query)
            connection.commit()

        cursor.close()
        connection.close()

        end_time = time.time()
        result = dict(
            status='success',
            message=str(count) + ' rows has added to database successfully',
            payload=None,
            elapsed=str(datetime.timedelta(seconds=(end_time - start_time)))
        )
        return jsonify(result)

    except Exception as e:
        print(str(e))
        result = dict(
            status='failure',
            message=str(e),
            payload=None,
            elapsed='00:00:00.0'
        )
        return jsonify(result)

@app.route('/remove', methods=['DELETE'])
def remove_data():
    try:
        start_time = time.time()

        count = request.args['count']

        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = 'DELETE FROM people WHERE id IN(SELECT id FROM people ORDER BY RANDOM() LIMIT ' + str(count) + ');'
        cursor.execute(sql_query)
        connection.commit()
        cursor.close()
        connection.close()

        end_time = time.time()
        result = dict(
            status='success',
            message=str(count) + ' rows has deleted from database successfully',
            payload=None,
            elapsed=str(datetime.timedelta(seconds=(end_time - start_time)))
        )
        return jsonify(result)

    except Exception as e:
        print(str(e))
        result = dict(
            status='failure',
            message=str(e),
            payload=None,
            elapsed='00:00:00.0'
        )
        return jsonify(result)

@app.route('/remove-row', methods=['DELETE'])
def remove_row_data():
    try:
        start_time = time.time()

        row_id = request.args['id']

        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = 'DELETE FROM people WHERE id = ' + str(row_id) + ';'
        cursor.execute(sql_query)
        connection.commit()
        cursor.close()
        connection.close()

        print(sql_query)

        end_time = time.time()
        result = dict(
            status='success',
            message='row with id ' + row_id + ' has deleted from database successfully',
            payload=None,
            elapsed=str(datetime.timedelta(seconds=(end_time - start_time)))
        )
        return jsonify(result)

    except Exception as e:
        print(str(e))
        result = dict(
            status='failure',
            message=str(e),
            payload=None,
            elapsed='00:00:00.0'
        )
        return jsonify(result)

@app.route('/test_data')
def test_data():
    values = generate_data(random.randint(25, 310))

    return jsonify(values)

def generate_data(entries_count):
    values = []
    index_id = 0
    for x in range(entries_count):
        index_id = index_id + 1
        if(fake.pybool()):
            value = dict(
                id=index_id,
                firstName=fake.first_name_male(),
                lastName=fake.last_name_male(),
                age=random.randint(18, 60),
                employment=fake.job().replace("'", ''),
                location=fake.city().replace("'", ''),
                favoriteColor=fake.color_name(),
                petName=petname.name().title(),
                serverId=server_id,
                addTimestamp=datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S')
            )
            values.append(value)
        else:
            value = dict(
                id=index_id,
                firstName=fake.first_name_female(),
                lastName=fake.last_name_female(),
                age=random.randint(18, 60),
                employment=fake.job().replace("'", ''),
                location=fake.city().replace("'", ''),
                favoriteColor=fake.color_name(),
                petName=petname.name().title(),
                serverId=server_id,
                addTimestamp=datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S')
            )
            values.append(value)
    return values

def db_init():
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')