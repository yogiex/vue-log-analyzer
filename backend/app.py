# app.py (Flask program)

from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime, timedelta
import pandas as pd
import urllib.parse
import pytz
import glob
from sklearn.ensemble import IsolationForest
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import threading
import time
from queue import Queue
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import json
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder, Application
import asyncio
from dotenv import load_dotenv, dotenv_values
from telegram.error import TelegramError, NetworkError
from hypercorn.asyncio import serve
from hypercorn.config import Config
import joblib
import signal
import sys
import pymysql
load_dotenv()

app = Flask(__name__)
CORS(app)

db_config_source = {
    'host': os.getenv("hostname_source"),
    'user': os.getenv("db_username_source"),
    'password': os.getenv("password_source"),
    'database': os.getenv("database_source"),
}

daftar_peserta = []
kumpulan_predict = []
output_queue = Queue()
BASE_DIR = "/home/linux/backup-sql"

data_summary = [
    {
        'total_case'   : 0,
        'total_label_0': 0,
        'total_label_1': 0,
        'total_user'   : 0,
        'total_case_monthly': [
            {
                'januari'  : 0,
                'februari' : 0,
                'maret'    : 0,
                'april'    : 0,
                'mei'      : 0,
                'juni'     : 0,
                'juli'     : 0,
                'agustus'  : 0,
                'september': 0,
                'oktober'  : 0,
                'november' : 0,
                'desember' : 0
            }
        ]    
    }
]

dynamic_settings = {
    "listening_timetaken" : 0,
    "listening_minscore" : 0,
    "grammar_timetaken" : 0,
    "grammar_minscore" : 0,
    "reading_timetaken" : 0,
    "reading_minscore" : 0
}

class peserta:
  def __init__(self, firstname, lastname, userid, timestart, timefinish, score, session, shift):
    self.firstname = firstname
    self.lastname = lastname
    self.userid = userid
    self.timestart = datetime.fromtimestamp(timestart, pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')
    self.timefinish = datetime.fromtimestamp(timefinish, pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')
    self.timetaken = datetime.fromtimestamp(timefinish - timestart, pytz.timezone('UTC')).strftime('%H:%M:%S')
    self.timedate = datetime.fromtimestamp(timestart, pytz.timezone('Asia/Jakarta'))
    self.timestart_unix = timestart
    self.score = score
    self.session = session
    self.status = 1
    self.track_progress = "secure"
    self.shift = shift

proctor_id = []

# Telegram bot setup
TOKEN = os.getenv("token")
# application = None

async def help(update: Update, context: CallbackContext) -> None:
    text = """
Selamat Datang di EPrT Log Analyzer, bot ini adalah bot notifikasi yang terintegrasi dengan log analyzer\n
berikut perintah yang dapat digunakan:
/help             - Menampilkan pesan ini
/daftar           - Menambahkan anda sebagai penerima pesan notifikasi bot
/daftarproktor    - Menampilkan proktor yang terdaftar sebagai penerima pesan notifikasi
/hapusproktor     - Menghapus diri dari daftar penerima pesan notifikasi
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def echo(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def getproctors(update: Update, context: CallbackContext) -> None:
    try:
        connection = mysql.connector.connect(**db_config_source)
    
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT chat_id FROM daftar_proktor"

            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            list_proctor_terdaftar = []

            for row in rows:
                list_proctor_terdaftar.append(row)
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=list_proctor_terdaftar)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Function to send messages asynchronously
async def send_message(chat_id: str, message: str):
    await application.bot.send_message(chat_id=chat_id, text=message)

# Function to send messages to all chat IDs
async def send_message_to_all(chat_ids, message):
    tasks = [send_message(chat_id, message) for chat_id in chat_ids]
    await asyncio.gather(*tasks)

async def daftar(update: Update, context: CallbackContext) -> None:
    try:
        connection = mysql.connector.connect(**db_config_source)
        chat_id = update.effective_chat.id
    
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO daftar_proktor (chat_id) VALUES (%s)"""
            cursor.execute(insert_query, (chat_id,))
            connection.commit()
            message = "akun proktor berhasil ditambahkan, akun ini akan menerima notifikasi dari log analyzer"

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except Error as e:
        message = "Akun ini sudah terdaftar sebagai proktor!"
        print("Error while connecting to MySQL", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

async def hapusproktor(update: Update, context: CallbackContext) -> None:
    try:
        connection = mysql.connector.connect(**db_config_source)
        chat_id = update.effective_chat.id
    
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """DELETE FROM daftar_proktor WHERE chat_id = (%s)"""
            cursor.execute(insert_query, (chat_id,))
            connection.commit()
            message = "akun ini berhasil dihapus dari daftar proktor! Akun ini tidak akan menerima pesan dari log analyzer"

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except Error as e:
        message = "Akun ini tidak terdaftar sebagai proktor!"
        print("Error while connecting to MySQL", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def getproctorforresult():
    try:
        connection = mysql.connector.connect(**db_config_source)
        cursor = connection.cursor()

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT chat_id FROM daftar_proktor"

            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            list_proctor_terdaftar = []

            for row in rows:
                list_proctor_terdaftar.append(row[0])
            
        return list_proctor_terdaftar

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def returnCheaterList(session):
    list_curang = []
    message_list =[]
    for p in daftar_peserta:
        if p.status == "terindikasi":
            list_curang.append(p)
    
    for individu in list_curang:
        temp_list = [individu.firstname, individu.lastname]
        message_list.append(temp_list)

    waktu = datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%Y/%m/%d %H:%M:%S')

    message_head = f"Tanggal {waktu}\n\n"
    message_footer = f"\n\nPeserta berikut terindikasi melakukan kecurangan pada sesi {session}!"
    message_daftar_curang = '\n'.join([' '.join(sublist) for sublist in message_list])

    if message_daftar_curang == None or message_daftar_curang == '':
        pass
    else:
        message = message_head + message_daftar_curang + message_footer
        # Run the asynchronous function
        asyncio.run(send_message_to_all(getproctorforresult(), message))

def get_time_shift():
    # Define Indonesian month names
    month_names_id = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]
    timezone = pytz.timezone('Asia/Jakarta')

    # Get current time
    current_time = datetime.now()

    # Format current time with Indonesian month name
    formatted_date = current_time.strftime(f"%d {month_names_id[current_time.month - 1]} %Y")
    formatted_time = current_time.astimezone(timezone)

    # Determine phase based on current hour
    if 8 <= formatted_time.hour <= 10:
        shift = "Shift 1"
    elif 11 <= formatted_time.hour <= 13:
        shift = "Shift 2"
    elif 14 <= formatted_time.hour <= 16:
        shift = "Shift 3"
    else:
        shift = "Shift 4"
    
    return formatted_date, shift

def get_shift(time):
    timezone = pytz.timezone('Asia/Jakarta')
    time = datetime.fromtimestamp(time)
    formatted_time = time.astimezone(timezone)

    if 7 <= formatted_time.hour <= 9:
        shift = "Shift 1"
    elif 10 <= formatted_time.hour <= 12:
        shift = "Shift 2"
    elif 13 <= formatted_time.hour <= 16:
        shift = "Shift 3"
    else:
        shift = "Shift 4"

    return shift

def get_sql_data():
    conn = mysql.connector.connect(**db_config_source)
    cursor = conn.cursor()

    try:
        # Get the current date and time
        current_time = datetime.now()

        # Define the test times (7 AM, 11 AM, 2 PM) as UNIX timestamps
        test_times = [
            datetime.combine(current_time.date(), datetime.min.time()) + timedelta(hours=7),
            datetime.combine(current_time.date(), datetime.min.time()) + timedelta(hours=11),
            datetime.combine(current_time.date(), datetime.min.time()) + timedelta(hours=14)
        ]

        # Convert test times to UNIX format
        test_times_unix = [int(time.timestamp()) for time in test_times]

        # Determine which test data to retrieve based on the current time
        if current_time < test_times[1]:
            selected_test_time = test_times_unix[0]
        elif current_time < test_times[2]:
            selected_test_time = test_times_unix[1]
        else:
            selected_test_time = test_times_unix[2]

        #query =
        #    SELECT id_peserta, firstname, lastname, quiz_name, unique_id, timestart, timefinish, score 
        #    FROM backup_attempt
        #    WHERE timestart >= %s AND timestart < %s;
        #
        query = """
            SELECT id_peserta, firstname, lastname, quiz_name, unique_id, timestart, timefinish, score 
            FROM backup_attempt;
            """

        # selected_test_time = 1724842800

        next_test_time = selected_test_time + 4 * 60 * 60  # Add 4 hours to cover the entire time range

        cursor.execute("""SELECT id_peserta, firstname, lastname, quiz_name, unique_id, 
                       timestart, timefinish, score FROM backup_attempt""")

        # cursor.execute(query, (selected_test_time, next_test_time))

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        return rows, columns
    
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")
    

def create_dataframe():
    # data_dir = 'downloaded_files'
    # list_file = glob.glob(data_dir)

    # if len(list_file) == 1:
    #     data = 'downloaded_files/Listening.xlsx'
    #     session = 'listening'
    # elif len(list_file) == 2:
    #     data = 'downloaded_files/Grammar.xlsx'
    #     session = 'grammar'
    # elif len(list_file) == 3:
    #     data = 'downloaded_files/Reading.xlsx'
    #     session = 'reading'

    # data = 'downloaded_files/Grammar.xlsx'
    # session = 'grammar'

    data, columns = get_sql_data()
    # session = None

    for row in data:
        if "listening".lower() in row[3].lower():
            session = "listening"
        elif "grammar".lower() in row[3].lower():
            session = "grammar"
        elif "reading".lower() in row[3].lower():
            session = "reading"

    # session = "grammar"
    df_data = pd.DataFrame(data, columns=columns)
    # df_data = pd.read_excel('downloaded_files\Grammar.xlsx')

    return session, df_data

def getPeserta(df_data, session):

    for index, row in df_data.iterrows():
        # Check if the userid is already in daftar_peserta
        # if not any(p.userid == row['id_peserta'] for p in daftar_peserta):
        newPeserta = peserta(row['firstname'], row['lastname'], row['id_peserta'], row['timestart'], 
                                row['timefinish'], row['score'], session, get_shift(row['timestart']))
        daftar_peserta.append(newPeserta)

    # Convert 'timestart' and 'timefinish' to datetime if needed
    df_data['timestart'] = pd.to_datetime(df_data['timestart'])
    df_data['timefinish'] = pd.to_datetime(df_data['timefinish'])

    # Calculate time difference and convert to minutes
    df_data['diff_time'] = df_data['timefinish'] - df_data['timestart']
    df_data['diff_time_minute'] = df_data['diff_time'].dt.total_seconds() / 60

def add_value(row):
    if "Grammar".lower() in row['quiz_name'].lower():
        grammar_diff_time_minute = row['diff_time_minute']
        return grammar_diff_time_minute / 25
    elif "Reading".lower() in row['quiz_name'].lower():
        reading_diff_time_minute = row['diff_time_minute']
        return reading_diff_time_minute / 55
    elif "Listening".lower() in row['quiz_name'].lower():
        listening_diff_time_minute = row['diff_time_minute']
        return listening_diff_time_minute / 35
    
def predict(df_data, session):
  if session == 'listening':
    df_data['listening_diff_time_minute'] = 0.0
    df_data['listening_completion_ratio'] = 0.0
    df_data['listening_score'] = 0

    for index, row in df_data.iterrows():
        df_data.loc[index, 'listening_diff_time_minute'] = row['diff_time_minute']
        df_data.loc[index, 'listening_completion_ratio'] = add_value(row)
        df_data.loc[index, 'listening_score'] = row['score']

    # Selecting relevant features
    features = df_data[['listening_diff_time_minute', 'listening_completion_ratio', 'listening_score']]

    # Fitting the Isolation Forest
    iso_forest_listening = joblib.load('./models/Listening_iso_forest_model.pkl')
    df_data['anomaly_score_iso'] = iso_forest_listening.fit_predict(features)

  elif session == 'reading':
    df_data['reading_diff_time_minute'] = 0.0
    df_data['reading_completion_ratio'] = 0.0
    df_data['reading_score'] = 0

    for index, row in df_data.iterrows():
        df_data.loc[index, 'reading_diff_time_minute'] = row['diff_time_minute']
        df_data.loc[index, 'reading_completion_ratio'] = add_value(row)
        df_data.loc[index, 'reading_score'] = row['score']

    # Selecting relevant features
    features = df_data[['reading_diff_time_minute', 'reading_completion_ratio', 'reading_score']]

    # Fitting the Isolation Forest
    iso_forest_reading = joblib.load('./models/Reading_iso_forest_model.pkl')
    df_data['anomaly_score_iso'] = iso_forest_reading.fit_predict(features)

  elif session == 'grammar':
    df_data['grammar_diff_time_minute'] = 0.0
    df_data['grammar_completion_ratio'] = 0.0
    df_data['grammar_score'] = 0

    for index, row in df_data.iterrows():
        df_data.loc[index, 'grammar_diff_time_minute'] = row['diff_time_minute']
        df_data.loc[index, 'grammar_completion_ratio'] = add_value(row)
        df_data.loc[index, 'grammar_score'] = row['score']

    # Selecting relevant features
    features = df_data[['grammar_diff_time_minute', 'grammar_completion_ratio', 'grammar_score']]

    # Fitting the Isolation Forest
    iso_forest_grammar = joblib.load('./models/Grammar_iso_forest_model.pkl')
    df_data['anomaly_score_iso'] = iso_forest_grammar.fit_predict(features)

def add_pred_value(df_data, session):
   for index, row in df_data.iterrows():
    for p in daftar_peserta:
        if p.userid == row['id_peserta']:
            p.status = row['anomaly_score_iso']
            # if p.status == -1:
                # if session == 'listening' or session == 'reading':
            if session == 'reading':
                nilai_max = 50
                treshold_nilai = dynamic_settings['reading_minscore']
                treshold_time = dynamic_settings['reading_timetaken']
            elif session == 'grammar':
                nilai_max = 40
                treshold_nilai = dynamic_settings['grammar_minscore']
                treshold_time = dynamic_settings['grammar_timetaken']
            elif session == 'listening':
                nilai_max = 1
                treshold_nilai = dynamic_settings['listening_minscore']
                treshold_time = dynamic_settings['grammar_timetaken']

            converted_nilai = (p.score / nilai_max) * 100
            converted_treshold = (treshold_nilai / nilai_max) * 100
            if converted_nilai < 40:
                p.status = 1

            time_str = p.timetaken
            hours, minutes, seconds = map(int, time_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            total_seconds = duration.total_seconds()

            if total_seconds < treshold_time:
             if p.score > converted_treshold:
               p.status = -1

def doConcurrentPredict(df_data, session):
    batch_analysis_res = []
    final_res = []

    for i in range(5):
        predict(df_data, session)
        if i < 4:
            temp_df = df_data
            kumpulan_predict.append(temp_df)
            temp_df = None
        else:
            final_df = df_data
    
    for pred in kumpulan_predict:
        analysis_res = []
        for index, row in pred.iterrows():
            analysis_res.append(row['anomaly_score_iso'])
        batch_analysis_res.append(analysis_res)

    for sec_iterate in range(len(batch_analysis_res[0])):
        cheating_sum, honest_sum = 0, 0

        for iterate in range(len(batch_analysis_res)):

            if batch_analysis_res[iterate][sec_iterate] == 1:
                honest_sum += 1
            else:
                cheating_sum += 1

        if honest_sum > cheating_sum:
            final_res.append(1)
        else:
            final_res.append(0)
    
    for index, row in df_data.iterrows():
        row['anomaly_score_iso'] = final_res[index]

def getCaseCounts(daftar_peserta):
    cases, cheat, good = 0, 0, 0

    for p in daftar_peserta:
        if p.status == "terindikasi":
            cases += 1
            cheat += 1
        else:
            good += 1

    return cases, cheat, good

def getMonthlyCases(daftar_peserta):
    month_names_id = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]

    for p in daftar_peserta:
        if p.status == "terindikasi":
            data_summary[0]['total_case_monthly'][0][month_names_id[p.timedateUser.month - 1].lower()] += 1

    # for p in daftar_peserta:
    #     if p.status == -1:
    #         if p.timedateUser.month == 1:
    #             data_summary[0]['total_case_monthly'][0]['januari'] += 1
    #         elif p.timedateUser.month == 2:
    #             data_summary[0]['total_case_monthly'][0]['februari'] += 1
    #         elif p.timedateUser.month == 3:
    #             data_summary[0]['total_case_monthly'][0]['maret'] += 1
    #         elif p.timedateUser.month == 4:
    #             data_summary[0]['total_case_monthly'][0]['april'] += 1
    #         elif p.timedateUser.month == 5:
    #             data_summary[0]['total_case_monthly'][0]['mei'] += 1
    #         elif p.timedateUser.month == 6:
    #             data_summary[0]['total_case_monthly'][0]['juni'] += 1
    #         elif p.timedateUser.month == 7:
    #             data_summary[0]['total_case_monthly'][0]['juli'] += 1
    #         elif p.timedateUser.month == 8:
    #             data_summary[0]['total_case_monthly'][0]['agustus'] += 1
    #         elif p.timedateUser.month == 9:
    #             data_summary[0]['total_case_monthly'][0]['september'] += 1
    #         elif p.timedateUser.month == 10:
    #             data_summary[0]['total_case_monthly'][0]['oktober'] += 1
    #         elif p.timedateUser.month == 11:
    #             data_summary[0]['total_case_monthly'][0]['november'] += 1
    #         elif p.timedateUser.month == 12:
    #             data_summary[0]['total_case_monthly'][0]['desember'] += 1

def createSummary():
    cases, cheat, good = getCaseCounts(daftar_peserta)

    # actual data: cheat = -1, good =1
    # this function input: 0 = 1 (good), 1 = -1 (cheat)

    data_summary[0]['total_case'] = cases
    data_summary[0]['total_label_0'] = good
    data_summary[0]['total_label_1'] = cheat
    data_summary[0]['total_user'] = len(daftar_peserta)

    getMonthlyCases(daftar_peserta)

def renameStatusAndTrack(daftar_peserta):
    for p in daftar_peserta:
        if p.status == 1:
            p.status = "aman"
        else:
            p.status = "terindikasi"
            p.track_progress = "open"

def insertCasesToSQL(list_curang):

    data_json_response = jsonify(list_curang)
    data_json = data_json_response.get_json()
    data_json_str = json.dumps(data_json)
    
    try:
        connection = mysql.connector.connect(**db_config_source)
    
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO case_history (Cases) VALUES (%s)"""
            cursor.execute(insert_query, (data_json_str,))
            connection.commit()
            print("Record inserted successfully into your_table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    
def fetchCasesfromSQL():
    try:
        connection = mysql.connector.connect(**db_config_source)
    
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT Cases FROM case_history"

            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            temp_json = []
            json_data_list = []

            for row in rows:
                json_data = row[0]
                temp_json.append(json.loads(json_data))

            for datas in temp_json:
                json_data_list.extend(datas)

            return json_data_list

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insertHistoryToSQL(p):
    timedate = datetime.fromtimestamp(p.timestart_unix, pytz.timezone('Asia/Jakarta')).strftime('%y-%m-%d %H:%M:%S')
    timestart = datetime.fromtimestamp(p.timestart_unix, pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')

    try:
        connection = mysql.connector.connect(**db_config_source)
    
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO peserta_history 
            (firstname, lastname, userid, timedate, timestart, timefinish, timetaken, score, _session, _status, shift)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (p.firstname, p.lastname, p.userid, timedate,
                           timestart, p.timefinish, p.timetaken, p.score, p.session, p. status, p.shift)
            cursor.execute(insert_query, params)
            connection.commit()
            print("Record inserted successfully into your_table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def fetchHistoryfromSQL(param=None):
    try:
        connection = mysql.connector.connect(**db_config_source)
    
        if connection.is_connected():
            cursor = connection.cursor()

            if param is None or param == "":
                query = "SELECT * FROM peserta_history"

                cursor.execute(query)
            else:
                param = urllib.parse.unquote(param)
                param = param.replace('"', '')
                name_parts = param.split()
                if len(name_parts) == 1:
                    query = 'SELECT * FROM peserta_history WHERE firstname LIKE %s OR lastname LIKE %s'
                    args = [f'%{name_parts[0]}%', f'%{name_parts[0]}%']

                else:
                    firstname = name_parts[0]
                    lastname_parts = name_parts[1:]
                    
                    # Construct the query to handle both possible cases
                    query = 'SELECT * FROM peserta_history WHERE (firstname LIKE %s AND lastname LIKE %s)'
                    args = [f'%{firstname}%', '']
                    
                    for part in lastname_parts:
                        query += ' OR (firstname LIKE %s AND lastname LIKE %s)'
                        args += [f'%{part}%', f'%{part}%']

                    # Additional case to match if the parts are swapped
                    if lastname_parts:
                        query += ' OR (firstname LIKE %s AND lastname LIKE %s)'
                        args += [f'%{lastname_parts[0]}%', f'%{firstname}%']
    
            cursor.execute(query, args)
            rows = cursor.fetchall()

            json_data_history_list = []

            for row in rows:
                timedate =  row[4].strftime('%Y-%m-%d %H:%M:%S')
                timestart = format_timedelta(row[5])
                timefinish =format_timedelta(row[6])
                timetaken = format_timedelta(row[7])

                data = {'userid' :row[3], 'firstname': row[1], 'lastname': row[2], 'timedate': timedate,
                'timestart' : timestart, 'timefinish' : timefinish, 'time_taken' : timetaken, 
                'score' : row[8], 'status' : row[10], 'session': row[9], 'shift' : row[11]}

                json_data_history_list.append(data)

            return json_data_history_list
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def format_timedelta(td):
    seconds = td.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def clearPeserta(daftar_peserta):
    daftar_peserta.clear()

def delete_files_in_directory(directory):
    # Get the list of files in the directory
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        try:
            os.remove(file_path)  # Delete the file
            # print(f'Deleted: {file_path}')
        except Exception as e:
            print(f'Failed to delete: {file_path}, Error: {e}')

def download_folder_with_auth(url, download_dir, username, password):
    # Authenticate using basic auth
    auth = requests.auth.HTTPBasicAuth(username, password)

    # Get the contents of the folder (list of files)
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            file_name = link['href']
            if file_name.endswith('.xlsx'):  # Filter only Excel files, adjust as needed
                file_url = urljoin(url, file_name)
                file_path = os.path.join(download_dir, file_name)
                download_file(file_url, file_path, auth=auth)
        # print('Folder downloaded successfully.')
    else:
        print(f'Failed to download folder. Status code: {response.status_code}')

def download_file(file_url, file_path, auth=None):
    # Download the file
    response = requests.get(file_url, auth=auth)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        # print(f'Downloaded: {file_path}')
    else:
        print(f'Failed to download file: {file_url}')

def download_data_loop():
    while True:
        waktu, shift = get_time_shift()
        get_data(waktu, shift)
        time.sleep(10)

def start_background_task():
    task_thread = threading.Thread(target=download_data_loop)
    task_thread.daemon = True  # This makes sure the thread will exit when the main program exits
    task_thread.start()

def run_flask():
    app.run(host="0.0.0.0", port=8443, debug=True, use_reloader=False)
    # config = Config()
    # config.bind = ["localhost:8443"]
    # await serve(app, config)

async def run_bot():
    # Start the bot
    global application

    application = ApplicationBuilder().token(TOKEN).build()

    await application.initialize()

    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('daftarproctor', getproctors))
    application.add_handler(CommandHandler('daftar', daftar))
    application.add_handler(CommandHandler('hapusproctor', hapusproktor))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    await application.start()
    await application.updater.start_polling()

    # Keep the bot running until manually stopped
    await application.stop()

# Function to handle graceful shutdown
def shutdown(signum, frame):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True))
    sys.exit(0)

def flask_thread():
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

def shutdown_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def signal_handler(signal, frame):
    print("\nCtrl+C received! Shutting down gracefully...")
    
    # Shutdown Flask
    shutdown_flask()
    
    # Cancel asyncio loop
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.call_soon_threadsafe(loop.stop)

def main():
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

     # Start Flask in a new thread
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.start()
    
    # asyncio.run(run_bot())
    
    # Run the Telegram bot using asyncio
    # loop = asyncio.get_event_loop()
    # try:
    #     # Create and start the bot task
    #     bot_task = loop.create_task(run_bot())
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     # Gracefully stop the event loop
    #     loop.stop()
    #     bot_task.cancel()
    #     loop.run_until_complete(bot_task)
    #     loop.close()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Telegram bot must run in the main thread to handle signals properly
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('getproctor', getproctors))
    application.add_handler(CommandHandler('daftar', daftar))
    application.add_handler(CommandHandler('hapusproktor', hapusproktor))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot's polling in the main thread
    asyncio.run(application.run_polling())

    # Wait for the Flask thread to complete (this will not actually happen in normal execution)
    flask_thread.join()
        
# Route to display usernames and IP addresses
@app.route('/')
def show_usernames():
    clearPeserta(daftar_peserta)
    session, df_data = create_dataframe()
    getPeserta(df_data, session)
    
    # predict(df_data, session)
    doConcurrentPredict(df_data, session)            
                
    add_pred_value(df_data, session)
    renameStatusAndTrack(daftar_peserta)

    returnCheaterList(session)

    return render_template('usernames_test.html', user_data=daftar_peserta)

@app.route('/api/daftar_peserta', methods=['GET'])
def post_peserta():
    clearPeserta(daftar_peserta)
    session, df_data = create_dataframe()
    getPeserta(df_data, session)
    predict(df_data, session)
    add_pred_value(df_data, session)

    # renameStatusAndTrack(daftar_peserta)
    # createSummary()

    list_data = []
    list_curang = []
    for p in daftar_peserta:
        data = {'userid' : p.userid, 'firstname': p.firstname, 'lastname': p.lastname, 'timedate': p.timedate ,
                'timestart' : p.timestart, 'timefinish' : p.timefinish, 'time_taken' : p.timetaken, 
                'score' : p.score, 'status' : p.status, 'session': p.session, 'track_progress': p.track_progress,
                'shift' : p.shift}
        
        insertHistoryToSQL(p)

        if p.status == "terindikasi":
            list_curang.append(data)
        list_data.append(data)

    # insertCasesToSQL(list_curang)

    message = "The daftar peserta route was accessed!"  # Customize your message here
    
    # Run the asynchronous function
    asyncio.run(send_message_to_all(proctor_id, message))
    
    return jsonify(list_data)

@app.route('/peserta_history', methods=['GET'])
def getPesertaHistory():
    query = request.args.get('query', '').lower()
    data_history = fetchHistoryfromSQL(query)

    return jsonify(data_history)

@app.route('/get_summary', methods=['GET'])
def getSummary():

    return jsonify(data_summary)

@app.route('/api/get_cases', methods=['GET'])
def getCases():
    data_cases = fetchCasesfromSQL()

    return jsonify(data_cases)

@app.route('/detail_peserta', methods=['GET']) 
def show_detail_peserta():
    clearPeserta(daftar_peserta)
    session, df_data = create_dataframe()
    getPeserta(df_data, session)
    predict(df_data, session)
    add_pred_value(df_data, session)

    renameStatusAndTrack(daftar_peserta)

    # for p in daftar_peserta:
    #     p.firstname = "user"
    #     if p.status == 1:
    #         p.status = "honest"
    #         p.lastname = "name_1"
    #     else:
    #         p.status = "possibly cheating"
    #         p.lastname = "name_2"

    list_data = []
    for p in daftar_peserta:
        if p.status == 'aman':
            data = {'userid' : p.userid, 'firstname': 'user', 'lastname': 'name_1',
                    'timestart' : p.timestart, 'timefinish' : p.timefinish, 'time_taken' : p.timetaken, 
                    'score' : p.score, 'status' : 'honest', 'session': p.session}
        else:
            data = {'userid' : p.userid, 'firstname': 'user', 'lastname': 'name_2',
                    'timestart' : p.timestart, 'timefinish' : p.timefinish, 'time_taken' : p.timetaken, 
                    'score' : p.score, 'status' : 'possibly cheating', 'session': p.session}
        list_data.append(data)

    # return render_template('usernames_test.html', user_data=daftar_peserta)
    
    return jsonify(list_data)

@app.route('/dump', methods=['POST'])
def dump():
    #os.system('./bash/export-sql.sh')
    os.system('ssh -i /home/linux/.ssh/vm-a -p224 mirage@180.250.135.10 "/home/mirage/tes-dump-sql/bash/export-sql.sh" ')
    return ("berhasil")

@app.route('/backupfiles', methods=['GET'])
def backupfiles():
    
    return ("kuru kuru")

@app.route('/treshold-settings', methods=['POST'])
def modifytreshold():
    dynamic_settings['listening_timetaken'] = int(request.args.get("listening-timetaken")) * 60
    dynamic_settings['listening_minscore'] = int(request.args.get("listening-minscore"))
    dynamic_settings['grammar_timetaken'] = int(request.args.get("grammar-timetaken")) * 60
    dynamic_settings['grammar_minscore'] = int(request.args.get("grammar-minscore"))
    dynamic_settings['reading_timetaken'] = int(request.args.get("reading-timetaken")) * 60
    dynamic_settings['reading_minscore'] = int(request.args.get("reading-minscore"))

    return jsonify(dynamic_settings)

@app.route('/directory', defaults={'subdir': ''})
@app.route('/directory/<path:subdir>')
def list_backups(subdir):
    # Build the full path of the directory
    full_path = os.path.join(BASE_DIR, subdir)
    
    # Check if the path exists and is a directory
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return jsonify({"error": "Directory not found"}), 404
    
    # List the contents of the directory
    files = []
    for entry in os.listdir(full_path):
        entry_path = os.path.join(full_path, entry)
        if os.path.isfile(entry_path):
            # For files, return the full path and title
            files.append({
                "title": entry,
                "fullpath": os.path.join(full_path, entry),
                "url": request.host_url + 'download/' + os.path.join(subdir, entry)
            })
        elif os.path.isdir(entry_path):
            # For directories, allow recursion
            files.append({
                "title": entry + "/",
                "fullpath": os.path.join(full_path, entry),
                "url": request.host_url + 'directory/' + os.path.join(subdir, entry)
            })
    
    return jsonify(files)
@app.route('/download/<path:filename>')
def download_file(filename):
    # Build the full path to the file
    file_path = os.path.join(BASE_DIR, filename)

    # Normalize the path to prevent directory traversal
    file_path = os.path.normpath(file_path)

    # Check if the file exists and is within the base directory
    if not os.path.exists(file_path) or not os.path.isfile(file_path) or not file_path.startswith(os.path.normpath(BASE_DIR)):
        return jsonify({"error": "File not found"}), 404

    # Send the file for download
    return send_file(file_path, as_attachment=True)

# Database connection details for VM-A (Moodle database)
DB_CONFIG_VM_A = {
    'host': os.getenv('MYSQL_HOST_VM_A'),       # Replace with the IP of VM-A
    'user': os.getenv('MYSQL_USER_VM_A'),    # Replace with your Moodle database user
    'password': os.getenv('MYSQL_PASS_VM_A'),   # Replace with your Moodle database password
    'database': os.getenv('MYSQL_DB_VM_A')   # Replace with your Moodle database name
}

@app.route('/monitor/user-steps', methods=['GET'])
def monitor_user_steps():
    """
    Endpoint to fetch user step activity data from the Moodle database.
    Query parameters:
      - course_id: ID of the course (default: 4)
      - limit: Number of records to fetch (default: 100)
    """
    try:
        # Get query parameters
        course_id = request.args.get('course_id', type=int, default=4)
        limit = request.args.get('limit', type=int, default=100)

        # Connect to the database on VM-A
        connection = pymysql.connect(**DB_CONFIG_VM_A)

        # SQL query to fetch step activity
        query = f"""
        SELECT
            qa.id AS attempt_id,
            u.id AS user_id,
            u.firstname,
            u.lastname,
            c.fullname AS course_name,
            q.name AS quiz_name,
            qa.uniqueid,
            qa.timestart,
            qa.timefinish,
            qa.sumgrades AS score,
            qat.id AS question_attempt_id,
            qas.id AS step_id,
            qas.state AS step_state,
            qas.timecreated AS step_start_time,
            next_step.timecreated AS next_step_time,
            next_step.timecreated - qas.timecreated AS time_spent_on_question
        FROM
            mdl_quiz_attempts qa
        JOIN
            mdl_user u ON qa.userid = u.id
        JOIN
            mdl_quiz q ON qa.quiz = q.id
        JOIN
            mdl_course c ON q.course = c.id
        JOIN
            mdl_course_modules cm ON q.id = cm.instance AND cm.module = (SELECT id FROM mdl_modules WHERE name = 'quiz')
        JOIN
            mdl_question_attempts qat ON qa.uniqueid = qat.questionusageid
        JOIN
            mdl_question_attempt_steps qas ON qat.id = qas.questionattemptid
        LEFT JOIN
            mdl_question_attempt_steps next_step ON qas.questionattemptid = next_step.questionattemptid AND qas.sequencenumber = next_step.sequencenumber - 1
        WHERE
            c.id = {course_id}
        ORDER BY
            qa.timefinish DESC, qat.id, qas.timecreated
        LIMIT {limit};
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        connection.close()

        # Return the fetched data as JSON
        return jsonify({'status': 'success', 'data': results})

    except Exception as e:
        # Handle errors and return a JSON response
        return jsonify({'status': 'error', 'message': str(e)}), 500

def fetch_data_from_vm_a():
    """
    Fetch data from VM-A using the SELECT query.
    Returns:
        List of rows fetched from the database.
    """
    SELECT_QUERY = """
    SELECT 
        qa.id AS attempt_id,
        u.id AS id_peserta,
        u.firstname,
        u.lastname,
        c.fullname AS course_name,
        q.name AS quiz_name,
        qa.uniqueid AS unique_id,
        qa.layout,
        qa.timestart,
        qa.timefinish,
        qa.sumgrades AS score
    FROM
        mdl_quiz_attempts qa
    JOIN
        mdl_user u ON qa.userid = u.id
    JOIN
        mdl_quiz q ON qa.quiz = q.id
    JOIN
        mdl_course c ON q.course = c.id
    JOIN
        mdl_course_modules cm ON q.id = cm.instance AND cm.module = (SELECT id FROM mdl_modules WHERE name = 'quiz')       
    WHERE
        qa.state = 'finished'
    AND (cm.id = 9 OR cm.id = 10 OR cm.id = 11)
    ORDER BY
        qa.timefinish DESC;
    """
    try:
        connection = pymysql.connect(**DB_CONFIG_VM_A)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(SELECT_QUERY)
            results = cursor.fetchall()
        connection.close()
        return results
    except Exception as e:
        raise Exception(f"Error fetching data from VM-A: {e}")

def insert_data_into_vm_b(data):
    """
    Insert data into VM-B using the INSERT query.
    Args:
        data: List of rows to insert into the backup_attempt table.
    """
    INSERT_QUERY = """
    INSERT INTO backup_attempt (
        attempt_id,
        id_peserta,
        firstname,
        lastname,
        course_name,
        quiz_name,
        unique_id,
        layout,
        timestart,
        timefinish,
        score
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        connection = pymysql.connect(**db_config_source)
        with connection.cursor() as cursor:
            cursor.executemany(INSERT_QUERY, data)
            connection.commit()
        connection.close()
    except Exception as e:
        raise Exception(f"Error inserting data into VM-B: {e}")

@app.route('/api/sync-attempts', methods=['POST'])
def sync_attempts():
    """
    API endpoint to fetch data from VM-A and insert into VM-B.
    """
    try:
        # Step 1: Fetch data from VM-A
        fetched_data = fetch_data_from_vm_a()

        # Step 2: Format data for insertion into VM-B
        formatted_data = [
            (
                row['attempt_id'],
                row['id_peserta'],
                row['firstname'],
                row['lastname'],
                row['course_name'],
                row['quiz_name'],
                row['unique_id'],
                row['layout'],
                row['timestart'],
                row['timefinish'],
                row['score'],
            )
            for row in fetched_data
        ]

        # Step 3: Insert data into VM-B
        if formatted_data:
            insert_data_into_vm_b(formatted_data)

        return jsonify({"status": "success", "message": "Data synchronized successfully.", "rows_synced": len(formatted_data)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/get/logs', methods=['GET'])
def get_logs():
    try:
        # Get time range from request
        start_time = request.args.get('start_time', type=int)
        end_time = request.args.get('end_time', type=int)

        if not start_time or not end_time:
            return jsonify({"error": "Both start_time and end_time are required"}), 400

        # SQL query
        query = f"""
        SELECT
            sl.id AS log_id,
            u.id AS user_id,
            u.firstname AS user_firstname,
            u.lastname AS user_lastname,
            c.fullname AS course_name,
            sl.component,
            sl.action,
            sl.target,
            sl.ip,
            q.id AS quiz_id,
            q.name AS quiz_name,
            sl.timecreated
        FROM
            mdl_logstore_standard_log sl
        JOIN
            mdl_user u ON sl.userid = u.id
        JOIN
            mdl_course c ON sl.courseid = c.id
        LEFT JOIN
            mdl_quiz q ON sl.objecttable = 'quiz' AND sl.objectid = q.id
        WHERE
            c.id = 4
            AND sl.timecreated BETWEEN {start_time} AND {end_time}
        ORDER BY
            sl.id DESC;
        """

        # Connect to the database
        connection = pymysql.connect(**DB_CONFIG_VM_A)
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        # Process and return results
        logs = [
            {
                "log_id": row[0],
                "user_id": row[1],
                "user_firstname": row[2],
                "user_lastname": row[3],
                "course_name": row[4],
                "component": row[5],
                "action": row[6],
                "target": row[7],
                "ip": row[8],
                "quiz_id": row[9],
                "quiz_name": row[10],
                "timecreated": row[11],
            }
            for row in results
        ]

        return jsonify(logs), 200  # Return the logs array directly

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Count Directory
def count_directories(path):
    """Count the number of directories in the given path."""
    try:
        return len([entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))])
    except FileNotFoundError:
        return 0  # Return 0 if the directory does not exist

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """API endpoint to get the summary of users and mdl_standard_logs."""
    try:
        # Connect to the database
        connection = pymysql.connect(
	    host = os.getenv('MYSQL_HOST_VM_A'),      
            user = os.getenv('MYSQL_USER_VM_A'),    
            password = os.getenv('MYSQL_PASS_VM_A'),   
            database = os.getenv('MYSQL_DB_VM_A'),
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Query for count of users
            cursor.execute("SELECT COUNT(*) AS count FROM mdl_user;")
            count_users = cursor.fetchone()['count']

            # Query for count of mdl_standard_logs
            cursor.execute("SELECT COUNT(*) AS count FROM mdl_logstore_standard_log;")
            count_mdl_standard_logs = cursor.fetchone()['count']
            # Query for count of total steps
            # Query for total_count_step
            cursor.execute("""
                SELECT COUNT(*) AS total_count_step
                FROM (
                    SELECT
                        qa.id AS attempt_id,
                        u.id AS user_id,
                        u.firstname,
                        u.lastname,
                        c.fullname AS course_name,
                        q.name AS quiz_name,
                        qa.uniqueid,
                        qa.timestart,
                        qa.timefinish,
                        qa.sumgrades AS score,
                        qat.id AS question_attempt_id,
                        qas.id AS step_id,
                        qas.state AS step_state,
                        qas.timecreated AS step_start_time,
                        next_step.timecreated AS next_step_time,
                        next_step.timecreated - qas.timecreated AS time_spent_on_question
                    FROM
                        mdl_quiz_attempts qa
                    JOIN
                        mdl_user u ON qa.userid = u.id
                    JOIN
                        mdl_quiz q ON qa.quiz = q.id
                    JOIN
                        mdl_course c ON q.course = c.id
                    JOIN
                        mdl_course_modules cm ON q.id = cm.instance 
                        AND cm.module = (SELECT id FROM mdl_modules WHERE name = 'quiz')
                    JOIN
                        mdl_question_attempts qat ON qa.uniqueid = qat.questionusageid
                    JOIN
                        mdl_question_attempt_steps qas ON qat.id = qas.questionattemptid
                    LEFT JOIN
                        mdl_question_attempt_steps next_step ON qas.questionattemptid = next_step.questionattemptid 
                        AND qas.sequencenumber = next_step.sequencenumber - 1
                    WHERE
                        c.id = 4
                ) AS subquery;
            """)
            total_count_step = cursor.fetchone()['total_count_step']
        # Close the connection after executing the queries
        connection.close()
        # Count directories in the base directory
        directory_count = count_directories(BASE_DIR)

        # Return the summary as JSON
        return jsonify({
            "count_users": count_users,
            "count_mdl_standard_logs": count_mdl_standard_logs,
            "count_total_steps": total_count_step,
            "count_directory": directory_count
        })

    except pymysql.MySQLError as e:
        # Handle database connection or query errors
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        # Handle other errors
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Telegram bot must run in the main thread to handle signals properly
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('daftarproctor', getproctors))
    application.add_handler(CommandHandler('daftar', daftar))
    application.add_handler(CommandHandler('hapusproktor', hapusproktor))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot's polling in the main thread
    asyncio.run(application.run_polling())

    # Wait for the Flask thread to complete
    flask_thread.join()
