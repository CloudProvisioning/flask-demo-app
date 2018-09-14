from flask import Flask, render_template, jsonify
import psycopg2
import json
import random
import os

app = Flask(__name__)

def get_db_connection():
    dbname = 'test'
    dbuser = 'test'
    dbhost = '192.168.203.158'
    dbport = 31280

    connection = psycopg2.connect(database=dbname, user=dbuser, host=dbhost, port=dbport)
    return connection

@app.route('/')
def index():

    return render_template('home.htm')

@app.route('/get_all_countries')
def get_all_countries(entries=None):
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, capital FROM world")
    entries = cursor.fetchall()

    # return json.dumps(entries)
    return jsonify(entries)

@app.route('/get_top10_most_populated')
def get_top10_most_populated(entries=None):
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, population FROM world ORDER BY population DESC LIMIT 10")
    entries = cursor.fetchall()

    return jsonify(entries)

@app.route('/get_flag_of_random_country')
def get_flag_of_random_country(entry=None):
    
    cursor = get_db_connection().cursor()
    cursor.execute("SELECT name, flag FROM world")
    entries = cursor.fetchall()
    entry = entries[random.randint(0, len(entries) - 1)]

    return jsonify(entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')