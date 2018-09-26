from flask import Flask, render_template, request, escape, url_for, json, redirect, jsonify, session
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
import sqlite3
import datetime

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB',}
@app.route('/login')
def do_login() -> str:
   session['logged_in'] = True
   return render_template('login.html')

@app.route('/logout')
def do_logout() -> str:
   session.pop('logged_in')
   return 'You are nou logged out.'

   

def sql_insert(key_id, human_name) -> None:
    time_now = datetime.datetime.now()

    _SQL = """insert into Hystory (KeyID, humanID, timeGave) 
    values (?, (select humanID from Humans where humanName = ?),?)"""

    _SQL2 = """update Chei set Stare_ID = 2 where Chei.Ch_ID = ?"""

    _SQL3 = """select case when Chei.Stare_ID=1 then 'TRUE' else 'FALSE' end from Chei where Ch_ID =? """

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    cursor.execute(_SQL3, (key_id,))
    stare_now = cursor.fetchall()
    for item in stare_now:
        if item[0] == 'TRUE':
            cursor.execute(_SQL, (key_id, human_name, time_now,))
            cursor.execute(_SQL2, (key_id,))
    conn.commit()
    conn.close()


def filter(etaj_num):
    _SQL = """select Ch_ID, St_name, Humans.humanName, max(timeGave) from
    Hystory, Chei,Humans, stari where Chei.Stare_ID =2
    and keyID = Ch_Id and Humans.humanID=Hystory.humanID and Stari.Stare_ID= Chei.Stare_ID and Etaj_ID =? group by Ch_ID"""

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    cursor.execute(_SQL, (etaj_num,))
    stare = cursor.fetchall()
    conn.close()
    return stare


def get_time_insert(Key_id) -> None:
    time_now = datetime.datetime.now()

    _SQL = """update Hystory set timeBack =?
                where Hystory.KeyID = ?"""

    _SQL2 = """update Chei set Stare_ID = 1 where Chei.Ch_ID = ?"""

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    cursor.execute(_SQL, (time_now, Key_id))
    cursor.execute(_SQL2, (Key_id,))
    conn.commit()
    conn.close()


def chei_fill():
    _SQL = """select Ch_ID from Chei"""

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    cursor.execute(_SQL)
    results = cursor.fetchall()
    conn.close()
    return results


def person_fill():
    _SQL2 = """ select humanName from Humans"""

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    cursor.execute(_SQL2)
    humans = cursor.fetchall()
    conn.close()
    return humans


@app.route('/')
@app.route('/entry', methods=['GET', 'POST'])
def sql_query() -> 'html':
    results = chei_fill()
    humans = person_fill()
    stare = list()
    if request.method == 'POST':
        key_id = request.form.get('key_id')
        human_name = request.form.get('human_name')
        sql_insert(key_id, human_name)
        office_et = request.get_json()

        if len(str(office_et)) == 3:
            get_time_insert(office_et)
        elif len(str(office_et)) == 1:
            stare = filter(office_et)
            json_str = json.dumps(stare)
            return json_str
    else:

        office_et = 1
        stare = filter(office_et)

        return render_template('main.html', the_stare_data=stare, the_data=results, name_list=humans)
    return redirect(url_for('sql_query'))


def sql_report(key_id=None, human_name=None, date=None):
    _SQL = """select keyID, Humans.humanName, timeGave, timeBack from
    Hystory,  Humans"""

    where_st1 = """ where
    keyID = ? and Humans.humanID=Hystory.humanID and Humans.humanName =? and (select date(timeGave)) = ?"""

    where_st2 = """ where
    keyID = ? and Humans.humanID=Hystory.humanID and Humans.humanName =?"""

    where_st3 = """ where
    keyID = ? and Humans.humanID=Hystory.humanID and (select date(timeGave)) = ?"""

    where_st4 = """ where
     Humans.humanID=Hystory.humanID and Humans.humanName =? and (select date(timeGave)) = ?"""

    where_st5 = """ where
    keyID = ? and Humans.humanID=Hystory.humanID"""

    where_st6 = """ where
    Humans.humanID=Hystory.humanID and Humans.humanName =?"""

    where_st7 = """ where
    Humans.humanID=Hystory.humanID and (select date(timeGave)) = ? """

    conn = sqlite3.connect('keymanagerdb.db')
    cursor = conn.cursor()
    if key_id is not None:
        if human_name is not None:
            if date is not '':
                _SQL += where_st1
                cursor.execute(_SQL,(key_id, human_name, date,))
            else:
                _SQL += where_st2
                cursor.execute(_SQL,(key_id, human_name,)) 
        else:
            if date is not '':
                _SQL += where_st3
                cursor.execute(_SQL,(key_id, date,))
            else:
                _SQL += where_st5
                cursor.execute(_SQL,(key_id,))
    else:
        if human_name is not None:
            if date is not '':
                _SQL += where_st4
                cursor.execute(_SQL,(human_name, date,))
            else:
                _SQL += where_st6
                cursor.execute(_SQL,(human_name,)) 
        else:
            if date is not '':
                _SQL += where_st7
                cursor.execute(_SQL,(date,))

    key_inf = cursor.fetchall()
    conn.close()
    return key_inf


@app.route('/report', methods=['GET', 'POST'])
def report_main_function() -> 'html':
    results = chei_fill()
    humans = person_fill()
    if request.method == 'POST':
        key_id = request.form.get('key_id')
        human_name = request.form.get('human_name')
        date = request.form.get('date_time')
        if key_id is not None or human_name is not None or date is not None:
            report_inf = sql_report(key_id, human_name, date)
            return render_template('report.html', the_data=results, name_list=humans, the_stare_data=report_inf)
    else:
        return render_template('report.html', the_data=results, name_list=humans)

app.secret_key = '1234567890'
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
