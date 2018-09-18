from flask import Flask, render_template, jsonify
import psycopg2
import json
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    dbname = 'test'
    dbuser = 'test'
    # dbhost = '192.168.203.158'
    # dbport = 31280
    dbhost = 'mycockroach-cockroachdb-public'
    dbport = 26257

    connection = psycopg2.connect(database=dbname, user=dbuser, host=dbhost, port=dbport)
    return connection

@app.route('/')
def index():

    return jsonify([
        'Application is working!',
        'Available APIs:',
        '/get_all_countries',
        '/get_top10_most_populated',
        '/get_flag_of_random_country'
    ])

@app.route('/get_all_countries')
def get_all_countries():
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, capital, continent, area, population FROM world")
    entries = cursor.fetchall()

    result = []

    for item in entries:
        innerItem = dict(
            country=item[0],
            capital=item[1],
            continent=item[2],
            area=item[3],
            population=item[4]
        )
        result.append(innerItem)

    return jsonify(result)

@app.route('/get_top10_most_populated')
def get_top10_most_populated():
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, population FROM world ORDER BY population DESC LIMIT 10")
    entries = cursor.fetchall()

    result = []

    for item in entries:
        innerItem = dict(
            country=item[0],
            population=item[1],
        )
        result.append(innerItem)

    return jsonify(result)

@app.route('/get_flag_of_random_country')
def get_flag_of_random_country():
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, flag FROM world")
    entries = cursor.fetchall()
    entry = entries[random.randint(0, len(entries) - 1)]

    result = dict(
            country=entry[0],
            flagUrl=entry[1],
        )

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')